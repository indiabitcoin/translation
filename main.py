"""Main application entry point for LibreTranslate server."""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Header, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional
from pydantic import BaseModel

from app.config import settings
from app.models import (
    TranslateRequest,
    TranslateResponse,
    LanguageInfo,
    DetectRequest,
    DetectResponse,
    HealthResponse
)
from app.translation import TranslationService
from app.auth import (
    create_user, authenticate_user, get_user, update_user_usage,
    check_usage_limit, get_user_usage, upgrade_user_plan,
    generate_token, verify_token, get_user_by_api_key
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize translation service
translation_service = TranslationService(
    load_only=settings.allowed_languages,
    model_directory=settings.model_directory
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup
    logger.info("Starting LibreTranslate server...")
    logger.info(f"Configuration: host={settings.host}, port={settings.port}")
    
    if settings.allowed_languages:
        logger.info(f"Loading languages: {settings.allowed_languages}")
    
    # Auto-install models if enabled and none are installed
    update_models = settings.update_models
    if settings.auto_install_models:
        # Check if any models are installed
        try:
            import argostranslate.package
            installed = argostranslate.package.get_installed_packages()
            if not installed:
                logger.info("No models found. Auto-installing default models...")
                update_models = True
        except Exception as e:
            logger.warning(f"Could not check installed packages: {e}")
    
    success = translation_service.initialize(update_models=update_models)
    if not success:
        logger.error("Failed to initialize translation service")
        raise RuntimeError("Translation service initialization failed")
    
    logger.info("Server started successfully")
    
    yield  # Application runs here
    
    # Shutdown (if needed)
    logger.info("Shutting down server...")


# Create FastAPI app
app = FastAPI(
    title="LibreTranslate Server",
    description="Self-hosted translation server using LibreTranslate",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_api_key(api_key: Optional[str] = Header(None, alias="X-API-Key")) -> Optional[dict]:
    """Verify API key if required. Returns user dict if authenticated."""
    if not settings.api_key_required:
        # Check if user provided API key for usage tracking
        if api_key:
            user = get_user_by_api_key(api_key)
            return user
        return None
    
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    # Check user API keys first
    user = get_user_by_api_key(api_key)
    if user:
        return user
    
    # Check configured API keys
    valid_keys = settings.valid_api_keys
    if valid_keys and api_key in valid_keys:
        return None  # Valid system API key, no user tracking
    
    raise HTTPException(status_code=403, detail="Invalid API key")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="ok")


@app.get("/packages")
async def get_packages(user: Optional[dict] = Depends(verify_api_key)):
    """Get detailed information about installed translation packages (diagnostic endpoint)."""
    if not translation_service.is_initialized():
        raise HTTPException(
            status_code=503,
            detail="Translation service not available"
        )
    
    try:
        import argostranslate.package
        installed = argostranslate.package.get_installed_packages()
        
        packages_info = []
        for pkg in installed:
            packages_info.append({
                "from_code": pkg.from_code,
                "to_code": pkg.to_code,
                "package_name": getattr(pkg, 'package_name', 'unknown'),
                "package_version": getattr(pkg, 'package_version', 'unknown')
            })
        
        # Check model directory
        model_dir_info = {}
        if translation_service.model_directory:
            import os
            model_dir = translation_service.model_directory
            model_dir_info = {
                "path": model_dir,
                "exists": os.path.exists(model_dir),
                "is_symlink": os.path.islink(model_dir) if os.path.exists(model_dir) else False,
                "file_count": len(os.listdir(model_dir)) if os.path.exists(model_dir) and os.path.isdir(model_dir) else 0
            }
            
            # Check symlink target
            argos_dir = os.path.expanduser('~/.local/share/argos-translate/packages')
            if os.path.exists(argos_dir):
                if os.path.islink(argos_dir):
                    model_dir_info["symlink_target"] = os.readlink(argos_dir)
                model_dir_info["argos_packages_dir"] = argos_dir
                model_dir_info["argos_dir_exists"] = True
                if os.path.isdir(argos_dir):
                    model_dir_info["argos_dir_file_count"] = len(os.listdir(argos_dir))
        
        return {
            "total_packages": len(installed),
            "packages": packages_info,
            "model_directory": model_dir_info,
            "uk_languages": {
                "cy": any(p.from_code == "cy" or p.to_code == "cy" for p in installed),
                "gd": any(p.from_code == "gd" or p.to_code == "gd" for p in installed),
                "kw": any(p.from_code == "kw" or p.to_code == "kw" for p in installed),
                "gv": any(p.from_code == "gv" or p.to_code == "gv" for p in installed),
            }
        }
    except Exception as e:
        logger.error(f"Failed to get packages info: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve package information: {str(e)}")


@app.get("/languages", response_model=list[LanguageInfo])
async def get_languages(user: Optional[dict] = Depends(verify_api_key)):
    """Get list of supported languages."""
    languages = translation_service.get_languages()
    if languages is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve languages")
    
    # Convert to LanguageInfo format
    result = []
    for lang in languages:
        if isinstance(lang, dict):
            code = lang.get("code", "")
            name = lang.get("name", code)
            result.append(LanguageInfo(code=code, name=name))
        else:
            # Handle case where languages might be returned in different format
            logger.warning(f"Unexpected language format: {lang}")
    
    return result


@app.post("/translate", response_model=TranslateResponse)
async def translate(
    request: TranslateRequest,
    user: Optional[dict] = Depends(verify_api_key)
):
    """Translate text from source language to target language."""
    if not translation_service.is_initialized():
        raise HTTPException(
            status_code=503,
            detail="Translation service not available"
        )
    
    # Check usage limit for authenticated users
    if user:
        text_length = len(request.q)
        if not check_usage_limit(user['email'], text_length):
            limit = get_user_usage(user['email'])['limit']
            raise HTTPException(
                status_code=403,
                detail=f"Usage limit exceeded. Current plan allows {limit:,} characters per month. Please upgrade your plan."
            )
    
    translated_text, error_message = translation_service.translate(
        text=request.q,
        source=request.source,
        target=request.target,
        format_type=request.format
    )
    
    if translated_text is None:
        raise HTTPException(
            status_code=400,
            detail=error_message or "Translation failed"
        )
    
    # Update usage for authenticated users
    if user:
        update_user_usage(user['email'], len(request.q))
    
    return TranslateResponse(translatedText=translated_text)


@app.post("/detect", response_model=DetectResponse)
async def detect_language(
    request: DetectRequest,
    user: Optional[dict] = Depends(verify_api_key)
):
    """Detect the language of the given text."""
    if not translation_service.is_initialized():
        raise HTTPException(
            status_code=503,
            detail="Translation service not available"
        )
    
    result = translation_service.detect_language(request.q)
    
    if result is None:
        raise HTTPException(
            status_code=500,
            detail="Language detection failed"
        )
    
    # Handle different response formats
    if isinstance(result, dict):
        language = result.get("language", "")
        confidence = result.get("confidence", 0.0)
    else:
        # Fallback if result format is unexpected
        logger.warning(f"Unexpected detection result format: {result}")
        language = str(result) if result else ""
        confidence = 0.0
    
    return DetectResponse(language=language, confidence=confidence)


# Authentication Models
class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class UpgradeRequest(BaseModel):
    plan: str

# Authentication Endpoints
@app.post("/api/auth/signup")
async def signup(request: SignupRequest):
    """Create a new user account."""
    try:
        user = create_user(request.email, request.password, request.name)
        token = generate_token(user)
        
        # Remove sensitive data
        user_data = {k: v for k, v in user.items() if k != 'password_hash'}
        
        return {
            "token": token,
            "user": user_data,
            "usage": get_user_usage(request.email)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Signup error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create account")

@app.post("/api/auth/login")
async def login(request: LoginRequest):
    """Authenticate user and return token."""
    user = authenticate_user(request.email, request.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = generate_token(user)
    
    # Remove sensitive data
    user_data = {k: v for k, v in user.items() if k != 'password_hash'}
    
    return {
        "token": token,
        "user": user_data,
        "usage": get_user_usage(request.email)
    }

def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """Get current user from JWT token."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization required")
    
    try:
        token = authorization.replace("Bearer ", "")
        email = verify_token(token)
        
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = get_user(email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Auth error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/api/user/usage")
async def get_usage(user: dict = Depends(get_current_user)):
    """Get current user usage."""
    return get_user_usage(user['email'])

@app.post("/api/user/usage")
async def update_usage(request: dict, user: dict = Depends(get_current_user)):
    """Update user usage (internal use)."""
    # This is mainly for frontend to sync, actual usage is tracked in translate endpoint
    return get_user_usage(user['email'])

@app.post("/api/subscription/upgrade")
async def upgrade_subscription(request: UpgradeRequest, user: dict = Depends(get_current_user)):
    """Upgrade user subscription plan."""
    try:
        upgrade_user_plan(user['email'], request.plan)
        updated_user = get_user(user['email'])
        user_data = {k: v for k, v in updated_user.items() if k != 'password_hash'}
        
        return {
            "user": user_data,
            "usageLimit": get_user_usage(user['email'])['limit']
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Upgrade error: {e}")
        raise HTTPException(status_code=500, detail="Failed to upgrade plan")

# Serve static files
import os
static_dir = os.path.join(os.path.dirname(__file__), 'frontend')
css_dir = os.path.join(static_dir, 'css')
js_dir = os.path.join(static_dir, 'js')

if os.path.exists(css_dir):
    app.mount("/static/css", StaticFiles(directory=css_dir), name="css")
if os.path.exists(js_dir):
    app.mount("/static/js", StaticFiles(directory=js_dir), name="js")

@app.get("/")
async def serve_frontend():
    """Serve the frontend index page."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend not found. Please build the frontend."}


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {settings.host}:{settings.port}")
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
        log_level="info"
    )

