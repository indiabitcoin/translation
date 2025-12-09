#!/usr/bin/env python3
"""
Script to install community-contributed Argos Translate models.

Usage:
    python install_community_model.py --url <model_url> [--model-dir <directory>]
    python install_community_model.py --file <model_path> [--model-dir <directory>]
"""

import argparse
import sys
import os
import urllib.request
import tempfile
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

try:
    import argostranslate.package
except ImportError:
    logger.error("argostranslate package not installed. Install it with: pip install argostranslate")
    sys.exit(1)


def install_from_url(url: str, model_dir: Optional[str] = None) -> bool:
    """
    Download and install an Argos Translate model from a URL.
    
    Args:
        url: URL to the .argosmodel file
        model_dir: Optional custom directory for models
    
    Returns:
        True if installation successful, False otherwise
    """
    try:
        logger.info(f"Downloading model from {url}...")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.argosmodel') as tmp_file:
            tmp_path = tmp_file.name
        
        # Download the model
        urllib.request.urlretrieve(url, tmp_path)
        logger.info(f"Downloaded to {tmp_path}")
        
        # Install the model
        return install_from_file(tmp_path, model_dir)
    
    except Exception as e:
        logger.error(f"Failed to download/install from URL: {e}")
        return False
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except:
                pass


def install_from_file(file_path: str, model_dir: Optional[str] = None) -> bool:
    """
    Install an Argos Translate model from a local file.
    
    Args:
        file_path: Path to the .argosmodel file
        model_dir: Optional custom directory for models
    
    Returns:
        True if installation successful, False otherwise
    """
    try:
        if not os.path.exists(file_path):
            logger.error(f"Model file not found: {file_path}")
            return False
        
        if not file_path.endswith('.argosmodel'):
            logger.warning(f"File does not have .argosmodel extension: {file_path}")
        
        # Set custom model directory if provided
        if model_dir:
            os.makedirs(model_dir, exist_ok=True)
            # Argos Translate uses ~/.local/share/argos-translate/packages
            # Create symlink if needed
            argos_dir = os.path.expanduser('~/.local/share/argos-translate')
            os.makedirs(argos_dir, exist_ok=True)
            packages_dir = os.path.join(argos_dir, 'packages')
            
            if not os.path.exists(packages_dir):
                os.symlink(model_dir, packages_dir)
                logger.info(f"Created symlink: {packages_dir} -> {model_dir}")
        
        logger.info(f"Installing model from {file_path}...")
        argostranslate.package.install_from_path(file_path)
        
        logger.info("✅ Model installed successfully!")
        
        # Verify installation
        installed = argostranslate.package.get_installed_packages()
        logger.info(f"Total installed packages: {len(installed)}")
        
        return True
    
    except Exception as e:
        logger.error(f"Failed to install model: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Install community-contributed Argos Translate models',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Install from URL
  python install_community_model.py --url https://example.com/en-cy.argosmodel
  
  # Install from local file
  python install_community_model.py --file ./en-cy.argosmodel
  
  # Install to custom directory
  python install_community_model.py --url https://example.com/en-cy.argosmodel --model-dir /app/models
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', type=str, help='URL to download the .argosmodel file from')
    group.add_argument('--file', type=str, help='Path to local .argosmodel file')
    
    parser.add_argument(
        '--model-dir',
        type=str,
        default=None,
        help='Custom directory for storing models (default: ~/.local/share/argos-translate/packages)'
    )
    
    args = parser.parse_args()
    
    success = False
    if args.url:
        success = install_from_url(args.url, args.model_dir)
    elif args.file:
        success = install_from_file(args.file, args.model_dir)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

