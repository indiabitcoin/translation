#!/usr/bin/env python3
"""
Install additional non-English language pairs to maximize translation coverage.

This script installs language pairs that aren't English-based (e.g., es→fr, de→ja)
to increase the number of available translation directions.
"""

import sys
import os
from typing import Optional, Set, Tuple

try:
    import argostranslate.package
except ImportError:
    print("Error: argostranslate not installed. Install with: pip install argostranslate")
    sys.exit(1)


def setup_model_directory(model_dir: Optional[str] = None):
    """Set up model directory and symlink."""
    if model_dir:
        os.makedirs(model_dir, exist_ok=True)
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
            os.symlink(model_dir, packages_dir)
            print(f"✅ Created symlink: {packages_dir} -> {model_dir}")


def get_installed_pairs() -> Set[Tuple[str, str]]:
    """Get set of already installed language pairs."""
    installed = argostranslate.package.get_installed_packages()
    return set((p.from_code, p.to_code) for p in installed)


def install_more_pairs(model_dir: Optional[str] = None, dry_run: bool = False):
    """Install additional non-English language pairs."""
    print("="*70)
    print("INSTALLING ADDITIONAL NON-ENGLISH LANGUAGE PAIRS")
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
    
    # Get already installed pairs
    installed_pairs = get_installed_pairs()
    print(f"✅ Found {len(installed_pairs)} already installed pairs")
    
    # Filter to non-English pairs
    # Priority: Popular language pairs that aren't English-based
    priority_pairs = [
        # Major European language pairs
        ("es", "fr"), ("fr", "es"),  # Spanish ↔ French
        ("es", "de"), ("de", "es"),  # Spanish ↔ German
        ("es", "it"), ("it", "es"),  # Spanish ↔ Italian
        ("es", "pt"), ("pt", "es"),  # Spanish ↔ Portuguese (may already exist)
        ("fr", "de"), ("de", "fr"),  # French ↔ German
        ("fr", "it"), ("it", "fr"),  # French ↔ Italian
        ("fr", "pt"), ("pt", "fr"),  # French ↔ Portuguese
        ("de", "it"), ("it", "de"),  # German ↔ Italian
        ("de", "pt"), ("pt", "de"),  # German ↔ Portuguese
        ("it", "pt"), ("pt", "it"),  # Italian ↔ Portuguese
        
        # European to Asian
        ("es", "zh"), ("zh", "es"),  # Spanish ↔ Chinese
        ("fr", "zh"), ("zh", "fr"),  # French ↔ Chinese
        ("de", "zh"), ("zh", "de"),  # German ↔ Chinese
        ("es", "ja"), ("ja", "es"),  # Spanish ↔ Japanese
        ("fr", "ja"), ("ja", "fr"),  # French ↔ Japanese
        ("de", "ja"), ("ja", "de"),  # German ↔ Japanese
        ("es", "ko"), ("ko", "es"),  # Spanish ↔ Korean
        ("fr", "ko"), ("ko", "fr"),  # French ↔ Korean
        ("de", "ko"), ("ko", "de"),  # German ↔ Korean
        
        # Asian language pairs
        ("zh", "ja"), ("ja", "zh"),  # Chinese ↔ Japanese
        ("zh", "ko"), ("ko", "zh"),  # Chinese ↔ Korean
        ("ja", "ko"), ("ko", "ja"),  # Japanese ↔ Korean
        
        # Middle Eastern pairs
        ("ar", "fr"), ("fr", "ar"),  # Arabic ↔ French
        ("ar", "de"), ("de", "ar"),  # Arabic ↔ German
        ("ar", "es"), ("es", "ar"),  # Arabic ↔ Spanish
        ("ar", "tr"), ("tr", "ar"),  # Arabic ↔ Turkish
        ("ar", "fa"), ("fa", "ar"),  # Arabic ↔ Persian
        
        # Russian pairs
        ("ru", "de"), ("de", "ru"),  # Russian ↔ German
        ("ru", "fr"), ("fr", "ru"),  # Russian ↔ French
        ("ru", "es"), ("es", "ru"),  # Russian ↔ Spanish
        ("ru", "zh"), ("zh", "ru"),  # Russian ↔ Chinese
        ("ru", "ja"), ("ja", "ru"),  # Russian ↔ Japanese
        
        # More popular pairs
        ("pt", "fr"), ("fr", "pt"),  # Portuguese ↔ French
        ("pt", "de"), ("de", "pt"),  # Portuguese ↔ German
        ("pt", "it"), ("it", "pt"),  # Portuguese ↔ Italian
        ("nl", "de"), ("de", "nl"),  # Dutch ↔ German
        ("nl", "fr"), ("fr", "nl"),  # Dutch ↔ French
        ("pl", "de"), ("de", "pl"),  # Polish ↔ German
        ("pl", "ru"), ("ru", "pl"),  # Polish ↔ Russian
    ]
    
    # Find packages that match priority pairs and aren't installed
    packages_to_install = []
    for package in available_packages:
        pair = (package.from_code, package.to_code)
        if pair in priority_pairs and pair not in installed_pairs:
            packages_to_install.append(package)
    
    # Also add any other non-English pairs that aren't installed
    for package in available_packages:
        pair = (package.from_code, package.to_code)
        if (package.from_code != "en" and package.to_code != "en" and 
            pair not in installed_pairs and package not in packages_to_install):
            packages_to_install.append(package)
    
    print(f"\n📥 Found {len(packages_to_install)} additional packages to install")
    print("   (Non-English language pairs)")
    
    if dry_run:
        print("\n🔍 DRY RUN MODE - No packages will be installed")
        print(f"Would install {len(packages_to_install)} packages:")
        for i, pkg in enumerate(packages_to_install[:30], 1):
            print(f"   {i}. {pkg.from_code} -> {pkg.to_code}")
        if len(packages_to_install) > 30:
            print(f"   ... and {len(packages_to_install) - 30} more")
        return
    
    if not packages_to_install:
        print("\n✅ No additional packages to install (all non-English pairs already installed)")
        return
    
    print(f"\n📥 Installing {len(packages_to_install)} additional packages...")
    print("   (This may take a while - each package is 50-500MB)")
    
    installed_count = 0
    failed_count = 0
    failed_packages = []
    
    for i, package in enumerate(packages_to_install, 1):
        try:
            print(f"\n[{i}/{len(packages_to_install)}] Installing {package.from_code} -> {package.to_code}...")
            download_path = package.download()
            print(f"   ✅ Downloaded")
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
    print(f"✅ Successfully installed: {installed_count} additional packages")
    print(f"❌ Failed: {failed_count} packages")
    
    # Get final counts
    final_installed = argostranslate.package.get_installed_packages()
    all_languages = set()
    for pkg in final_installed:
        all_languages.add(pkg.from_code)
        all_languages.add(pkg.to_code)
    
    print(f"\n📦 Total installed packages: {len(final_installed)}")
    print(f"🌍 Total unique languages: {len(all_languages)}")
    print(f"   Languages: {', '.join(sorted(all_languages))}")
    
    if failed_packages:
        print(f"\n⚠️  Failed packages:")
        for from_code, to_code, error in failed_packages[:10]:
            print(f"   {from_code} -> {to_code}: {error}")
        if len(failed_packages) > 10:
            print(f"   ... and {len(failed_packages) - 10} more")
    
    print("\n✅ Installation complete!")
    print("   Restart your translation server to use the new models.")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Install additional non-English language pairs for maximum translation coverage"
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
        install_more_pairs(
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

