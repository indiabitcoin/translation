"""Configuration management for the LibreTranslate server."""
from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 5000
    
    # Translation Configuration
    load_only: Optional[str] = None
    update_models: bool = False
    auto_install_models: bool = True  # Auto-install models if missing
    
    # API Configuration
    api_key_required: bool = False
    api_keys: Optional[str] = None
    
    # CORS Configuration
    cors_origins: str = "*"
    
    # Model Storage (for Coolify/persistent volumes)
    model_directory: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def allowed_languages(self) -> Optional[List[str]]:
        """Get list of languages to load, if specified."""
        if self.load_only:
            return [lang.strip() for lang in self.load_only.split(",")]
        return None
    
    @property
    def valid_api_keys(self) -> Optional[List[str]]:
        """Get list of valid API keys."""
        if self.api_keys:
            return [key.strip() for key in self.api_keys.split(",")]
        return None
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list."""
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()

