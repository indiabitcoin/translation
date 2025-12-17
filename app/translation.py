"""Translation service using Argos Translate (the engine behind LibreTranslate)."""
from typing import Optional, List, Dict, Any
from collections import deque
import logging
import time

logger = logging.getLogger(__name__)

# Cache for recent error messages to reduce log spam
_error_cache: Dict[str, float] = {}
_ERROR_CACHE_TTL = 60  # Log same error at most once per 60 seconds

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
            # Create symlink to custom directory so models are found
            argos_dir = os.path.expanduser('~/.local/share/argos-translate')
            os.makedirs(argos_dir, exist_ok=True)
            packages_dir = os.path.join(argos_dir, 'packages')
            
            # Remove existing symlink or directory if it exists and is different
            if os.path.exists(packages_dir):
                if os.path.islink(packages_dir):
                    current_target = os.readlink(packages_dir)
                    if current_target != model_directory:
                        os.remove(packages_dir)
                        os.symlink(model_directory, packages_dir)
                        logger.info(f"Updated symlink: {packages_dir} -> {model_directory}")
                elif os.path.isdir(packages_dir) and not os.path.samefile(packages_dir, model_directory):
                    # If it's a directory (not a symlink), we can't replace it easily
                    # But we'll try to symlink anyway - Argos will use the symlink if it exists
                    logger.warning(f"Packages directory exists as regular directory: {packages_dir}")
            else:
                # Create symlink if it doesn't exist
                os.symlink(model_directory, packages_dir)
                logger.info(f"Created symlink: {packages_dir} -> {model_directory}")
    
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
                
                # Get languages to install from environment or use default comprehensive list
                # If INSTALL_ALL_LANGUAGES=true, install all available languages
                import os
                install_all = os.getenv("INSTALL_ALL_LANGUAGES", "false").lower() == "true"
                
                if install_all:
                    # Install ALL available language pairs
                    logger.info("INSTALL_ALL_LANGUAGES=true: Installing all available language pairs...")
                    packages_to_install = available_packages
                else:
                    # Default: Install comprehensive set of popular global languages
                    # Includes European + major world languages
                    supported_languages = [
                        # European languages
                        "en",   # English
                        "es",   # Spanish
                        "fr",   # French
                        "de",   # German
                        "it",   # Italian
                        "pt",   # Portuguese
                        "ru",   # Russian
                        "pl",   # Polish
                        "nl",   # Dutch
                        "el",   # Greek
                        "cs",   # Czech
                        "ro",   # Romanian
                        "hu",   # Hungarian
                        "sv",   # Swedish
                        "no",   # Norwegian
                        "nb",   # Norwegian Bokmål
                        "da",   # Danish
                        "fi",   # Finnish
                        "bg",   # Bulgarian
                        "hr",   # Croatian
                        "sr",   # Serbian
                        "sk",   # Slovak
                        "sl",   # Slovenian
                        "lt",   # Lithuanian
                        "lv",   # Latvian
                        "et",   # Estonian
                        "ga",   # Irish
                        "ca",   # Catalan
                        "uk",   # Ukrainian
                        "be",   # Belarusian
                        "is",   # Icelandic
                        "mk",   # Macedonian
                        "sq",   # Albanian
                        # Note: UK regional languages (cy, gd, kw, gv) are not available in default Argos Translate models
                        # They require custom trained models. See README for details.
                        # Major world languages
                        "zh",   # Chinese
                        "ja",   # Japanese
                        "ko",   # Korean
                        "ar",   # Arabic
                        "hi",   # Hindi
                        "tr",   # Turkish
                        "he",   # Hebrew
                        "th",   # Thai
                        "vi",   # Vietnamese
                        "id",   # Indonesian
                        "ms",   # Malay
                        "tl",   # Tagalog/Filipino
                        "sw",   # Swahili
                        "af",   # Afrikaans
                        "az",   # Azerbaijani
                        "eu",   # Basque
                        "bn",   # Bengali
                        "bs",   # Bosnian
                        "br",   # Breton
                        "eo",   # Esperanto
                        "fa",   # Persian/Farsi
                        "gl",   # Galician
                        "gu",   # Gujarati
                        "ha",   # Hausa
                        "haw",  # Hawaiian
                        "hy",   # Armenian
                        "ig",   # Igbo
                        "is",   # Icelandic
                        "jw",   # Javanese
                        "ka",   # Georgian
                        "km",   # Khmer
                        "kn",   # Kannada
                        "kk",   # Kazakh
                        "ky",   # Kyrgyz
                        "lo",   # Lao
                        "lb",   # Luxembourgish
                        "ml",   # Malayalam
                        "mr",   # Marathi
                        "mn",   # Mongolian
                        "my",   # Myanmar/Burmese
                        "ne",   # Nepali
                        "ps",   # Pashto
                        "pa",   # Punjabi
                        "si",   # Sinhala
                        "so",   # Somali
                        "su",   # Sundanese
                        "tg",   # Tajik
                        "ta",   # Tamil
                        "te",   # Telugu
                        "ur",   # Urdu
                        "uz",   # Uzbek
                        "yi",   # Yiddish
                        "yo",   # Yoruba
                        "zu",   # Zulu
                    ]
                    
                    # Filter packages to supported language pairs
                    packages_to_install = []
                    for package in available_packages:
                        if package.from_code in supported_languages and package.to_code in supported_languages:
                            packages_to_install.append(package)
                
                if packages_to_install:
                    logger.info(f"Installing {len(packages_to_install)} translation models...")
                    installed_count = 0
                    # Install all language pairs
                    for package in packages_to_install:
                        try:
                            logger.info(f"Downloading {package.from_code} -> {package.to_code}...")
                            download_path = package.download()
                            logger.info(f"Installing {package.from_code} -> {package.to_code}...")
                            argostranslate.package.install_from_path(download_path)
                            installed_count += 1
                            logger.info(f"Successfully installed: {package.from_code} -> {package.to_code}")
                        except Exception as e:
                            logger.warning(f"Failed to install {package.from_code}->{package.to_code}: {e}")
                    logger.info(f"Installed {installed_count} out of {len(packages_to_install)} language packages")
                else:
                    logger.warning("No matching packages found to install")
            
            # Get installed packages
            self._installed_packages = argostranslate.package.get_installed_packages()
            
            # Log detailed information about installed packages
            if self._installed_packages:
                logger.info(f"Found {len(self._installed_packages)} installed translation packages:")
                # Group by language codes
                all_languages = set()
                uk_languages = {"cy", "gd", "kw", "gv"}
                found_uk_languages = set()
                
                for pkg in self._installed_packages[:20]:  # Log first 20
                    all_languages.add(pkg.from_code)
                    all_languages.add(pkg.to_code)
                    if pkg.from_code in uk_languages or pkg.to_code in uk_languages:
                        found_uk_languages.add(pkg.from_code)
                        found_uk_languages.add(pkg.to_code)
                        logger.info(f"  ✓ {pkg.from_code} -> {pkg.to_code}")
                
                if len(self._installed_packages) > 20:
                    logger.info(f"  ... and {len(self._installed_packages) - 20} more packages")
                
                if found_uk_languages:
                    logger.info(f"✅ UK regional languages detected: {', '.join(sorted(found_uk_languages))}")
                else:
                    logger.info(f"Available languages: {', '.join(sorted(all_languages))}")
            else:
                logger.warning("No translation packages installed. Please install packages using:")
                logger.warning("  python -m argostranslate.update")
                logger.warning("Or set UPDATE_MODELS=true on first run")
                
                # Check if model directory exists and has files
                if self.model_directory:
                    import os
                    if os.path.exists(self.model_directory):
                        files = os.listdir(self.model_directory)
                        if files:
                            logger.warning(f"Model directory {self.model_directory} contains {len(files)} items but packages not detected.")
                            logger.warning("This might indicate a symlink issue or model format problem.")
                            logger.warning(f"Contents: {', '.join(files[:10])}")
            
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
            
            # Validate that we have a package for this language pair
            if not self._has_translation_package(source, target):
                error_key = f"no_package_{source}_{target}"
                if not self._should_log_error(error_key):
                    # Silently return None if we've logged this error recently
                    return None
                
                logger.error(f"No translation package available for {source} -> {target}")
                # Try to find an alternative path through intermediate languages
                alternative_path = self._find_translation_path(source, target)
                if alternative_path:
                    logger.info(f"Using alternative translation path: {' -> '.join(alternative_path)}")
                    # Translate through intermediate languages
                    current_text = text
                    for i in range(len(alternative_path) - 1):
                        from_lang = alternative_path[i]
                        to_lang = alternative_path[i + 1]
                        if not self._has_translation_package(from_lang, to_lang):
                            path_error_key = f"no_package_{from_lang}_{to_lang}"
                            if self._should_log_error(path_error_key):
                                logger.error(f"Alternative path failed: no package for {from_lang} -> {to_lang}")
                            return None
                        current_text = argostranslate.translate.translate(current_text, from_lang, to_lang)
                    return current_text
                else:
                    # Get available languages for better error message (only log once)
                    available_langs = self.get_languages()
                    available_codes = [lang["code"] for lang in available_langs] if available_langs else []
                    logger.error(
                        f"Cannot translate {source} -> {target}: no direct or indirect path available. "
                        f"Available languages: {', '.join(sorted(available_codes))}"
                    )
                    return None
            
            # Get the translation
            translated_text = argostranslate.translate.translate(text, source, target)
            
            if format_type == "html":
                # For HTML, we'd need to preserve tags, but argostranslate handles text
                # This is a simplified implementation
                logger.debug("HTML format requested, but only plain text translation is supported")
            
            return translated_text
        except AttributeError as e:
            # Handle the specific 'NoneType' object has no attribute 'code' error
            if "'NoneType' object has no attribute 'code'" in str(e) or "'NoneType' object has no attribute" in str(e):
                logger.error(f"Translation package not found for {source} -> {target}. Available packages: {self._get_available_language_pairs()}")
                return None
            raise
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            import traceback
            logger.debug(f"Translation error traceback: {traceback.format_exc()}")
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
            # Refresh installed packages list to get latest packages
            # This ensures we detect newly installed packages
            import argostranslate.package
            current_installed = argostranslate.package.get_installed_packages()
            
            languages_dict = {}
            
            # Get unique languages from installed packages
            for package in current_installed:
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
            
            # Update cached installed packages list
            self._installed_packages = current_installed
            
            return languages
        except Exception as e:
            logger.error(f"Failed to get languages: {e}")
            return None
    
    def _get_language_name(self, code: str) -> str:
        """Get human-readable language name from code."""
        # Comprehensive language names mapping
        language_names = {
            # European languages
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "pl": "Polish",
            "nl": "Dutch",
            "el": "Greek",
            "cs": "Czech",
            "ro": "Romanian",
            "hu": "Hungarian",
            "sv": "Swedish",
            "no": "Norwegian",
            "nb": "Norwegian Bokmål",
            "da": "Danish",
            "fi": "Finnish",
            "bg": "Bulgarian",
            "hr": "Croatian",
            "sr": "Serbian",
            "sk": "Slovak",
            "sl": "Slovenian",
            "lt": "Lithuanian",
            "lv": "Latvian",
            "et": "Estonian",
            "ga": "Irish",
            "ca": "Catalan",
            "uk": "Ukrainian",
            "be": "Belarusian",
            "is": "Icelandic",
            "mk": "Macedonian",
            "sq": "Albanian",
            # Note: UK regional languages (cy, gd, kw, gv) require custom models
            # Major world languages
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean",
            "ar": "Arabic",
            "hi": "Hindi",
            "tr": "Turkish",
            "he": "Hebrew",
            "th": "Thai",
            "vi": "Vietnamese",
            "id": "Indonesian",
            "ms": "Malay",
            "tl": "Tagalog",
            "sw": "Swahili",
            "af": "Afrikaans",
            "az": "Azerbaijani",
            "eu": "Basque",
            "bn": "Bengali",
            "bs": "Bosnian",
            "br": "Breton",
            "eo": "Esperanto",
            "fa": "Persian",
            "gl": "Galician",
            "gu": "Gujarati",
            "ha": "Hausa",
            "haw": "Hawaiian",
            "hy": "Armenian",
            "ig": "Igbo",
            "jw": "Javanese",
            "ka": "Georgian",
            "km": "Khmer",
            "kn": "Kannada",
            "kk": "Kazakh",
            "ky": "Kyrgyz",
            "lo": "Lao",
            "lb": "Luxembourgish",
            "ml": "Malayalam",
            "mr": "Marathi",
            "mn": "Mongolian",
            "my": "Myanmar",
            "ne": "Nepali",
            "ps": "Pashto",
            "pa": "Punjabi",
            "si": "Sinhala",
            "so": "Somali",
            "su": "Sundanese",
            "tg": "Tajik",
            "ta": "Tamil",
            "te": "Telugu",
            "ur": "Urdu",
            "uz": "Uzbek",
            "yi": "Yiddish",
            "yo": "Yoruba",
            "zu": "Zulu",
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
    
    def _should_log_error(self, error_key: str) -> bool:
        """
        Check if an error should be logged (to prevent log spam).
        Returns True if error should be logged, False if it was recently logged.
        """
        global _error_cache
        current_time = time.time()
        
        # Clean old entries
        _error_cache = {
            k: v for k, v in _error_cache.items()
            if current_time - v < _ERROR_CACHE_TTL
        }
        
        # Check if this error was recently logged
        if error_key in _error_cache:
            return False
        
        # Mark this error as logged
        _error_cache[error_key] = current_time
        return True
    
    def _has_translation_package(self, from_code: str, to_code: str) -> bool:
        """Check if a translation package exists for the given language pair."""
        if not self._initialized:
            return False
        
        for package in self._installed_packages:
            if package.from_code == from_code and package.to_code == to_code:
                return True
        return False
    
    def _get_available_language_pairs(self) -> List[str]:
        """Get list of available language pairs as strings."""
        if not self._initialized:
            return []
        
        pairs = []
        for package in self._installed_packages:
            pairs.append(f"{package.from_code}->{package.to_code}")
        return pairs
    
    def _find_translation_path(self, from_code: str, to_code: str, max_depth: int = 2) -> Optional[List[str]]:
        """
        Find a translation path through intermediate languages.
        Uses breadth-first search to find the shortest path.
        
        Args:
            from_code: Source language code
            to_code: Target language code
            max_depth: Maximum number of intermediate languages (default: 2)
        
        Returns:
            List of language codes representing the path, or None if no path found
        """
        if not self._initialized:
            return None
        
        # If direct path exists, use it
        if self._has_translation_package(from_code, to_code):
            return [from_code, to_code]
        
        # BFS to find shortest path
        # Queue: (current_lang, path_so_far)
        queue = deque([(from_code, [from_code])])
        visited = {from_code}
        
        while queue and len(queue[0][1]) <= max_depth + 1:
            current_lang, path = queue.popleft()
            
            # Check all packages that start from current_lang
            for package in self._installed_packages:
                if package.from_code == current_lang:
                    next_lang = package.to_code
                    
                    if next_lang == to_code:
                        # Found path!
                        return path + [to_code]
                    
                    if next_lang not in visited and len(path) < max_depth + 1:
                        visited.add(next_lang)
                        queue.append((next_lang, path + [next_lang]))
        
        return None

