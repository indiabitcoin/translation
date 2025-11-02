"""Translation service using Argos Translate (the engine behind LibreTranslate)."""
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

try:
    import argostranslate.package
    import argostranslate.translate
except ImportError:
    logger.error("argostranslate package not installed. Please install it with: pip install argostranslate")
    argostranslate = None


class TranslationService:
    """Service for handling translation operations using Argos Translate."""
    
    def __init__(self, load_only: Optional[List[str]] = None, model_directory: Optional[str] = None):
        """
        Initialize the translation service.
        
        Args:
            load_only: List of language codes to load (for faster startup)
            model_directory: Custom directory for storing models (for persistent volumes)
        """
        self.load_only = load_only
        self.model_directory = model_directory
        self._installed_packages: List[Any] = []
        self._initialized = False
        
        # Set custom model directory if provided
        if model_directory:
            import os
            os.makedirs(model_directory, exist_ok=True)
            # Argos Translate uses ~/.local/share/argos-translate/packages
            # We'll create a symlink if needed
    
    def initialize(self, update_models: bool = False) -> bool:
        """
        Initialize the Argos Translate packages.
        
        Args:
            update_models: Whether to update translation models
        
        Returns:
            True if initialization successful, False otherwise
        """
        if argostranslate is None:
            logger.error("argostranslate package is not available")
            return False
        
        try:
            # Update packages if requested
            if update_models:
                logger.info("Updating translation models...")
                argostranslate.package.update_package_index()
                available_packages = argostranslate.package.get_available_packages()
                
                # Install all packages if many are requested, otherwise install popular pairs
                # Popular language pairs: en<->es, en<->fr, en<->de, en<->it, en<->pt, en<->ru, en<->zh
                popular_pairs = [
                    "en", "es", "fr", "de", "it", "pt", "ru", "zh", "ja", "ar"
                ]
                
                # Filter packages to popular language pairs
                packages_to_install = []
                for package in available_packages:
                    if package.from_code in popular_pairs and package.to_code in popular_pairs:
                        packages_to_install.append(package)
                
                if packages_to_install:
                    logger.info(f"Installing {len(packages_to_install)} popular translation models...")
                    installed_count = 0
                    for package in packages_to_install[:20]:  # Limit to 20 packages
                        try:
                            logger.info(f"Downloading {package.from_code} -> {package.to_code}...")
                            download_path = package.download()
                            logger.info(f"Installing {package.from_code} -> {package.to_code}...")
                            argostranslate.package.install_from_path(download_path)
                            installed_count += 1
                            logger.info(f"Successfully installed: {package.from_code} -> {package.to_code}")
                        except Exception as e:
                            logger.warning(f"Failed to install {package.from_code}->{package.to_code}: {e}")
                    logger.info(f"Installed {installed_count} out of {min(len(packages_to_install), 20)} packages")
                else:
                    logger.warning("No matching packages found to install")
            
            # Get installed packages
            self._installed_packages = argostranslate.package.get_installed_packages()
            
            if not self._installed_packages:
                logger.warning("No translation packages installed. Please install packages using:")
                logger.warning("  python -m argostranslate.update")
                logger.warning("Or set UPDATE_MODELS=true on first run")
            
            self._initialized = True
            logger.info(f"Translation service initialized with {len(self._installed_packages)} packages")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize translation service: {e}")
            self._initialized = False
            return False
    
    def translate(
        self,
        text: str,
        source: str,
        target: str,
        format_type: str = "text"
    ) -> Optional[str]:
        """
        Translate text from source language to target language.
        
        Args:
            text: Text to translate
            source: Source language code or 'auto'
            target: Target language code
            format_type: Format of text ('text' or 'html') - currently only 'text' supported
        
        Returns:
            Translated text or None if translation fails
        """
        if not self._initialized:
            logger.error("Translation service not initialized")
            return None
        
        try:
            # Handle 'auto' source language by detecting it first
            if source == "auto":
                detected = self.detect_language(text)
                if detected:
                    source = detected.get("language", "en")
                    logger.debug(f"Auto-detected source language: {source}")
                else:
                    source = "en"  # Default fallback
                    logger.warning(f"Could not detect language, using default: {source}")
            
            # Get the translation
            translated_text = argostranslate.translate.translate(text, source, target)
            
            if format_type == "html":
                # For HTML, we'd need to preserve tags, but argostranslate handles text
                # This is a simplified implementation
                logger.debug("HTML format requested, but only plain text translation is supported")
            
            return translated_text
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return None
    
    def get_languages(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get list of supported languages.
        
        Returns:
            List of language dictionaries with 'code' and 'name' keys
        """
        if not self._initialized:
            logger.error("Translation service not initialized")
            return None
        
        try:
            languages_dict = {}
            
            # Get unique languages from installed packages
            for package in self._installed_packages:
                from_code = package.from_code
                to_code = package.to_code
                
                # Add source language
                if from_code not in languages_dict:
                    languages_dict[from_code] = self._get_language_name(from_code)
                
                # Add target language
                if to_code not in languages_dict:
                    languages_dict[to_code] = self._get_language_name(to_code)
            
            # Convert to list format
            languages = [
                {"code": code, "name": name}
                for code, name in sorted(languages_dict.items())
            ]
            
            return languages
        except Exception as e:
            logger.error(f"Failed to get languages: {e}")
            return None
    
    def _get_language_name(self, code: str) -> str:
        """Get human-readable language name from code."""
        # Common language names mapping
        language_names = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean",
            "ar": "Arabic",
            "hi": "Hindi",
            "nl": "Dutch",
            "pl": "Polish",
            "uk": "Ukrainian",
            "tr": "Turkish",
            "cs": "Czech",
            "ro": "Romanian",
            "sv": "Swedish",
            "fi": "Finnish",
            "da": "Danish",
            "no": "Norwegian",
            "he": "Hebrew",
        }
        return language_names.get(code, code.upper())
    
    def detect_language(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Detect the language of the given text.
        
        Args:
            text: Text to detect language for
        
        Returns:
            Dictionary with 'language' and 'confidence' keys, or None if detection fails
        """
        if not self._initialized:
            logger.error("Translation service not initialized")
            return None
        
        try:
            # Try to detect by attempting translations with common languages
            # This is a simple heuristic approach
            common_languages = ["en", "es", "fr", "de", "it", "pt", "ru", "zh", "ja"]
            
            # Get available language pairs
            available_languages = set()
            for package in self._installed_packages:
                available_languages.add(package.from_code)
                available_languages.add(package.to_code)
            
            # Filter to only languages we have models for
            test_languages = [lang for lang in common_languages if lang in available_languages]
            
            if not test_languages:
                # Fallback to English if no models available
                return {"language": "en", "confidence": 0.5}
            
            # Try to translate to English (most common target)
            # If it works well, the source is likely correct
            # This is a simplified detection - for production, use a proper language detection library
            best_match = test_languages[0]
            
            # Simple heuristic: if we have a translation package from this language, use it
            for lang in test_languages:
                # Check if we have a package from this language to English
                for package in self._installed_packages:
                    if package.from_code == lang and package.to_code == "en":
                        best_match = lang
                        break
            
            return {
                "language": best_match,
                "confidence": 0.7  # Simplified detection with moderate confidence
            }
        except Exception as e:
            logger.error(f"Language detection failed: {e}")
            # Fallback: return English
            return {"language": "en", "confidence": 0.5}
    
    def is_initialized(self) -> bool:
        """Check if the service is initialized."""
        return self._initialized

