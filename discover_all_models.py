#!/usr/bin/env python3
"""
Discover all available translation models from Argos Translate package index
and community sources.

This script helps identify all available language pairs to make the translation
service world-class with comprehensive regional language support.
"""

import json
import sys
from typing import List, Dict, Set
from collections import defaultdict

try:
    import argostranslate.package
except ImportError:
    print("Error: argostranslate not installed. Install with: pip install argostranslate")
    sys.exit(1)


def get_all_available_packages() -> List:
    """Fetch all available packages from Argos Translate package index."""
    print("Updating package index...")
    try:
        argostranslate.package.update_package_index()
    except Exception as e:
        print(f"Warning: Failed to update package index: {e}")
        print("Continuing with cached index...")
    
    print("Fetching available packages...")
    packages = argostranslate.package.get_available_packages()
    return packages


def get_installed_packages() -> List:
    """Get currently installed packages."""
    return argostranslate.package.get_installed_packages()


def analyze_language_coverage(packages: List) -> Dict:
    """Analyze language coverage from available packages."""
    languages = set()
    language_pairs = defaultdict(list)
    language_stats = defaultdict(int)
    
    for pkg in packages:
        from_code = pkg.from_code
        to_code = pkg.to_code
        languages.add(from_code)
        languages.add(to_code)
        language_pairs[from_code].append(to_code)
        language_stats[from_code] += 1
        language_stats[to_code] += 1
    
    return {
        "languages": sorted(languages),
        "language_pairs": dict(language_pairs),
        "language_stats": dict(language_stats),
        "total_packages": len(packages),
        "total_languages": len(languages)
    }


def get_regional_languages() -> Dict[str, List[str]]:
    """Define comprehensive list of regional languages by region."""
    return {
        "UK Regional": ["cy", "gd", "kw", "gv"],  # Welsh, Scottish Gaelic, Cornish, Manx
        "European Regional": [
            "br",  # Breton
            "oc",  # Occitan
            "co",  # Corsican
            "sc",  # Sardinian
            "rm",  # Romansh
            "wa",  # Walloon
            "fur", # Friulian
            "lad", # Ladino
        ],
        "African Languages": [
            "am",  # Amharic
            "ber", # Berber languages
            "ff",  # Fulah
            "kab", # Kabyle
            "wo",  # Wolof
            "xh",  # Xhosa
            "st",  # Southern Sotho
            "tn",  # Tswana
            "ve",  # Venda
            "ts",  # Tsonga
            "ss",  # Swati
            "nr",  # Northern Ndebele
            "nso", # Northern Sotho
        ],
        "Asian Regional": [
            "as",  # Assamese
            "or",  # Odia
            "mai", # Maithili
            "sat", # Santali
            "kok", # Konkani
            "mni", # Manipuri
            "bho", # Bhojpuri
            "mag", # Magahi
            "raj", # Rajasthani
            "sd",  # Sindhi
            "ks",  # Kashmiri
            "dz",  # Dzongkha
            "bo",  # Tibetan
        ],
        "Indigenous Languages": [
            "qu",  # Quechua
            "ay",  # Aymara
            "gn",  # Guarani
            "iu",  # Inuktitut
            "oj",  # Ojibwe
            "cr",  # Cree
            "nv",  # Navajo
            "haw", # Hawaiian
        ],
        "Other Regional": [
            "mt",  # Maltese
            "gd",  # Scottish Gaelic
            "cy",  # Welsh
            "kw",  # Cornish
            "gv",  # Manx
            "fo",  # Faroese
            "se",  # Northern Sami
            "sm",  # Samoan
            "to",  # Tongan
            "fj",  # Fijian
            "ty",  # Tahitian
            "mi",  # Maori
        ]
    }


def check_regional_language_availability(
    packages: List,
    regional_languages: Dict[str, List[str]]
) -> Dict[str, Dict]:
    """Check which regional languages are available in the package index."""
    available_languages = set()
    for pkg in packages:
        available_languages.add(pkg.from_code)
        available_languages.add(pkg.to_code)
    
    results = {}
    for region, languages in regional_languages.items():
        results[region] = {
            "available": [],
            "missing": [],
            "total": len(languages)
        }
        for lang in languages:
            if lang in available_languages:
                results[region]["available"].append(lang)
            else:
                results[region]["missing"].append(lang)
    
    return results


def generate_report(
    coverage: Dict,
    installed: List,
    regional_availability: Dict,
    output_file: str = None
):
    """Generate a comprehensive report."""
    report = {
        "summary": {
            "total_available_packages": coverage["total_packages"],
            "total_languages": coverage["total_languages"],
            "installed_packages": len(installed),
            "installed_languages": len(set(
                [p.from_code for p in installed] + [p.to_code for p in installed]
            ))
        },
        "all_available_languages": coverage["languages"],
        "language_statistics": coverage["language_stats"],
        "regional_language_availability": regional_availability,
        "top_languages_by_coverage": sorted(
            coverage["language_stats"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:20]
    }
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Report saved to: {output_file}")
    
    return report


def print_summary(report: Dict):
    """Print a human-readable summary."""
    print("\n" + "="*70)
    print("TRANSLATION MODEL DISCOVERY REPORT")
    print("="*70)
    
    summary = report["summary"]
    print(f"\n📦 Package Statistics:")
    print(f"   Available packages: {summary['total_available_packages']}")
    print(f"   Installed packages: {summary['installed_packages']}")
    print(f"   Available languages: {summary['total_languages']}")
    print(f"   Installed languages: {summary['installed_languages']}")
    
    print(f"\n🌍 Regional Language Availability:")
    for region, data in report["regional_language_availability"].items():
        available_count = len(data["available"])
        missing_count = len(data["missing"])
        total = data["total"]
        status = "✅" if missing_count == 0 else "⚠️" if available_count > 0 else "❌"
        print(f"   {status} {region}: {available_count}/{total} available")
        if data["available"]:
            print(f"      Available: {', '.join(data['available'])}")
        if data["missing"]:
            print(f"      Missing: {', '.join(data['missing'])}")
    
    print(f"\n🏆 Top 20 Languages by Package Coverage:")
    for lang, count in report["top_languages_by_coverage"]:
        print(f"   {lang}: {count} packages")
    
    print(f"\n📋 All Available Languages ({len(report['all_available_languages'])}):")
    print(f"   {', '.join(report['all_available_languages'])}")
    
    print("\n" + "="*70)


def main():
    """Main function."""
    print("🔍 Discovering all available translation models...")
    print("="*70)
    
    # Get all available packages
    packages = get_all_available_packages()
    print(f"✅ Found {len(packages)} available packages")
    
    # Get installed packages
    installed = get_installed_packages()
    print(f"✅ Found {len(installed)} installed packages")
    
    # Analyze coverage
    coverage = analyze_language_coverage(packages)
    
    # Check regional language availability
    regional_languages = get_regional_languages()
    regional_availability = check_regional_language_availability(
        packages,
        regional_languages
    )
    
    # Generate report
    report = generate_report(
        coverage,
        installed,
        regional_availability,
        output_file="model_discovery_report.json"
    )
    
    # Print summary
    print_summary(report)
    
    # Recommendations
    print("\n💡 Recommendations:")
    print("   1. Set INSTALL_ALL_LANGUAGES=true to install all available models")
    print("   2. Check COMMUNITY_MODELS.md for community-contributed models")
    print("   3. Review model_discovery_report.json for detailed analysis")
    print("   4. Consider training custom models for missing regional languages")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

