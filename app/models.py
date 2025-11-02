"""Pydantic models for API requests and responses."""
from pydantic import BaseModel, Field
from typing import Optional, List


class TranslateRequest(BaseModel):
    """Request model for translation."""
    q: str = Field(..., description="Text to translate")
    source: str = Field(default="auto", description="Source language code or 'auto'")
    target: str = Field(..., description="Target language code")
    format: str = Field(default="text", description="Format of the text (text or html)")
    api_key: Optional[str] = Field(None, description="API key for authentication")


class TranslateResponse(BaseModel):
    """Response model for translation."""
    translatedText: str = Field(..., description="Translated text")


class LanguageInfo(BaseModel):
    """Language information model."""
    code: str = Field(..., description="Language code")
    name: str = Field(..., description="Language name")


class DetectRequest(BaseModel):
    """Request model for language detection."""
    q: str = Field(..., description="Text to detect language for")
    api_key: Optional[str] = Field(None, description="API key for authentication")


class DetectResponse(BaseModel):
    """Response model for language detection."""
    confidence: float = Field(..., description="Confidence score")
    language: str = Field(..., description="Detected language code")


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Server status")

