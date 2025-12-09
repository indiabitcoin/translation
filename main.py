"""Main application entry point for LibreTranslate server."""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

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


def verify_api_key(api_key: Optional[str] = Header(None, alias="X-API-Key")) -> bool:
    """Verify API key if required."""
    if not settings.api_key_required:
        return True
    
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    valid_keys = settings.valid_api_keys
    if valid_keys and api_key not in valid_keys:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return True


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="ok")


@app.get("/packages")
async def get_packages(_: bool = Depends(verify_api_key)):
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
async def get_languages(_: bool = Depends(verify_api_key)):
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
    _: bool = Depends(verify_api_key)
):
    """Translate text from source language to target language."""
    if not translation_service.is_initialized():
        raise HTTPException(
            status_code=503,
            detail="Translation service not available"
        )
    
    translated_text = translation_service.translate(
        text=request.q,
        source=request.source,
        target=request.target,
        format_type=request.format
    )
    
    if translated_text is None:
        # Get available languages for helpful error message
        available_languages = translation_service.get_languages()
        available_codes = []
        if available_languages:
            available_codes = [lang.get("code", "") for lang in available_languages]
            available_codes = sorted([code for code in available_codes if code])
        
        error_detail = f"Translation failed: No translation model available for '{request.source}' -> '{request.target}'"
        
        if available_codes:
            error_detail += f". Available languages: {', '.join(available_codes)}. "
            error_detail += f"Use GET /languages to see all supported languages."
        else:
            error_detail += ". No translation models are installed. Please install models first."
        
        # Special message for UK regional languages
        uk_languages = {"cy": "Welsh", "gd": "Scottish Gaelic", "kw": "Cornish", "gv": "Manx"}
        if request.target in uk_languages:
            error_detail += f" Note: {uk_languages[request.target]} ({request.target}) requires a community model. "
            error_detail += "See COMMUNITY_MODELS.md for installation instructions."
        
        raise HTTPException(
            status_code=400,
            detail=error_detail
        )
    
    return TranslateResponse(translatedText=translated_text)


@app.post("/detect", response_model=DetectResponse)
async def detect_language(
    request: DetectRequest,
    _: bool = Depends(verify_api_key)
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

