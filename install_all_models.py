#!/usr/bin/env python3
"""
Install ALL available translation models from Argos Translate package index.

This script installs every available language pair to make the translation
service world-class with maximum language coverage.

Usage:
    python install_all_models.py [--model-dir /path/to/models] [--dry-run]
"""

import argparse
import sys
import os
from typing import Optional

try:
    import argostranslate.package
except ImportError:
    print("Error: argostranslate not installed. Install with: pip install argostranslate")
    sys.exit(1)


def setup_model_directory(model_dir: Optional[str] = None):
    """Set up model directory and symlink."""
    if model_dir:
        os.makedirs(model_dir, exist_ok=True)
        # Create symlink to Argos Translate expected location
        argos_dir = os.path.expanduser('~/.local/share/argos-translate')
        os.makedirs(argos_dir, exist_ok=True)
        packages_dir = os.path.join(argos_dir, 'packages')
        
        if os.path.exists(packages_dir):
            if os.path.islink(packages_dir):
                current_target = os.readlink(packages_dir)
                if current_target != model_dir:
                    os.remove(packages_dir)
                    os.symlink(model_dir, packages_dir)
                    print(f"✅ Updated symlink: {packages_dir} -> {model_dir}")
            else:
                print(f"⚠️  Warning: {packages_dir} exists as directory, not symlink")
        else:
            os.symlink(model_dir, packages_dir)
            print(f"✅ Created symlink: {packages_dir} -> {model_dir}")


def install_all_models(model_dir: Optional[str] = None, dry_run: bool = False):
    """Install all available translation models."""
    print("="*70)
    print("INSTALLING ALL AVAILABLE TRANSLATION MODELS")
    print("="*70)
    
    # Setup model directory
    if model_dir:
        setup_model_directory(model_dir)
    
    # Update package index
    print("\n📦 Updating package index...")
    try:
        argostranslate.package.update_package_index()
        print("✅ Package index updated")
    except Exception as e:
        print(f"⚠️  Warning: Failed to update package index: {e}")
        print("Continuing with cached index...")
    
    # Get all available packages
    print("\n🔍 Fetching available packages...")
    available_packages = argostranslate.package.get_available_packages()
    print(f"✅ Found {len(available_packages)} available packages")
    
    if dry_run:
        print("\n🔍 DRY RUN MODE - No packages will be installed")
        print(f"Would install {len(available_packages)} packages:")
        for i, pkg in enumerate(available_packages[:20], 1):
            print(f"   {i}. {pkg.from_code} -> {pkg.to_code}")
        if len(available_packages) > 20:
            print(f"   ... and {len(available_packages) - 20} more")
        return
    
    # Get already installed packages
    installed_packages = argostranslate.package.get_installed_packages()
    installed_pairs = set(
        (p.from_code, p.to_code) for p in installed_packages
    )
    print(f"✅ Found {len(installed_packages)} already installed packages")
    
    # Filter out already installed
    packages_to_install = [
        pkg for pkg in available_packages
        if (pkg.from_code, pkg.to_code) not in installed_pairs
    ]
    
    print(f"\n📥 Installing {len(packages_to_install)} new packages...")
    print("   (This may take a long time - each package is 50-500MB)")
    
    installed_count = 0
    failed_count = 0
    failed_packages = []
    
    for i, package in enumerate(packages_to_install, 1):
        try:
            print(f"\n[{i}/{len(packages_to_install)}] Installing {package.from_code} -> {package.to_code}...")
            download_path = package.download()
            print(f"   ✅ Downloaded: {download_path}")
            argostranslate.package.install_from_path(download_path)
            installed_count += 1
            print(f"   ✅ Installed successfully")
        except Exception as e:
            failed_count += 1
            failed_packages.append((package.from_code, package.to_code, str(e)))
            print(f"   ❌ Failed: {e}")
    
    # Summary
    print("\n" + "="*70)
    print("INSTALLATION SUMMARY")
    print("="*70)
    print(f"✅ Successfully installed: {installed_count} packages")
    print(f"❌ Failed: {failed_count} packages")
    print(f"📦 Total installed packages: {len(installed_packages) + installed_count}")
    
    if failed_packages:
        print(f"\n⚠️  Failed packages:")
        for from_code, to_code, error in failed_packages[:10]:
            print(f"   {from_code} -> {to_code}: {error}")
        if len(failed_packages) > 10:
            print(f"   ... and {len(failed_packages) - 10} more")
    
    # Get final installed packages
    final_installed = argostranslate.package.get_installed_packages()
    all_languages = set()
    for pkg in final_installed:
        all_languages.add(pkg.from_code)
        all_languages.add(pkg.to_code)
    
    print(f"\n🌍 Total languages supported: {len(all_languages)}")
    print(f"   Languages: {', '.join(sorted(all_languages))}")
    
    print("\n✅ Installation complete!")
    print("   Restart your translation server to use the new models.")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Install all available translation models from Argos Translate"
    )
    parser.add_argument(
        "--model-dir",
        type=str,
        default=None,
        help="Custom directory for storing models (default: ~/.local/share/argos-translate/packages)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be installed without actually installing"
    )
    
    args = parser.parse_args()
    
    try:
        install_all_models(
            model_dir=args.model_dir,
            dry_run=args.dry_run
        )
        return 0
    except KeyboardInterrupt:
        print("\n\n⚠️  Installation interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

