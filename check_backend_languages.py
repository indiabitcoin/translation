#!/usr/bin/env python3
"""Script to check what languages the backend actually supports."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.translation import TranslationService
import json

def main():
    print("Checking backend language support...")
    print("=" * 60)
    
    # Initialize translation service
    service = TranslationService()
    success = service.initialize(update_models=False)
    
    if not success:
        print("❌ Failed to initialize translation service")
        return
    
    # Get languages
    languages = service.get_languages()
    
    if not languages:
        print("❌ No languages found")
        return
    
    # Count languages
    print(f"\n✅ Total languages supported: {len(languages)}")
    print("\nSupported languages:")
    print("-" * 60)
    
    # Sort by code
    languages_sorted = sorted(languages, key=lambda x: x['code'])
    
    for lang in languages_sorted:
        print(f"  {lang['code']:6} - {lang['name']}")
    
    # Get language codes only
    codes = [lang['code'] for lang in languages_sorted]
    
    print("\n" + "=" * 60)
    print(f"Language codes ({len(codes)}):")
    print(", ".join(codes))
    
    # Save to JSON file
    output_file = "backend_languages.json"
    with open(output_file, 'w') as f:
        json.dump(languages_sorted, f, indent=2)
    
    print(f"\n✅ Language list saved to: {output_file}")
    
    # Check installed packages
    try:
        import argostranslate.package
        installed = argostranslate.package.get_installed_packages()
        print(f"\n📦 Installed translation packages: {len(installed)}")
        
        # Count unique language pairs
        pairs = set()
        for pkg in installed:
            pairs.add(f"{pkg.from_code}->{pkg.to_code}")
        
        print(f"📊 Unique language pairs: {len(pairs)}")
        
    except Exception as e:
        print(f"\n⚠️  Could not get package info: {e}")

if __name__ == "__main__":
    main()

