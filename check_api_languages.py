#!/usr/bin/env python3
"""Script to check what languages the API server supports by querying the API."""
import sys
import json
import requests
from typing import Optional, Dict, List

def check_api_languages(api_url: str = "https://api.shravani.group", api_key: Optional[str] = None) -> Dict:
    """
    Check what languages the API server supports.
    
    Args:
        api_url: Base URL of the API server
        api_key: Optional API key for authentication
    
    Returns:
        Dictionary with language information
    """
    headers = {}
    if api_key:
        headers["X-API-Key"] = api_key
    
    result = {
        "api_url": api_url,
        "status": "unknown",
        "languages": [],
        "language_count": 0,
        "packages": None,
        "error": None
    }
    
    # Check health first
    try:
        health_url = f"{api_url}/health"
        print(f"🔍 Checking API health: {health_url}")
        health_response = requests.get(health_url, timeout=10)
        if health_response.status_code == 200:
            print("✅ API server is healthy")
        else:
            print(f"⚠️  API health check returned status {health_response.status_code}")
    except Exception as e:
        print(f"⚠️  Could not check API health: {e}")
    
    # Get languages
    try:
        languages_url = f"{api_url}/languages"
        print(f"\n🔍 Fetching languages from: {languages_url}")
        response = requests.get(languages_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            languages = response.json()
            result["languages"] = languages
            result["language_count"] = len(languages)
            result["status"] = "success"
            print(f"✅ Successfully retrieved {len(languages)} languages")
        else:
            result["error"] = f"HTTP {response.status_code}: {response.text}"
            result["status"] = "error"
            print(f"❌ Failed to get languages: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.RequestException as e:
        result["error"] = str(e)
        result["status"] = "error"
        print(f"❌ Error connecting to API: {e}")
    
    # Get packages info (if available)
    try:
        packages_url = f"{api_url}/packages"
        print(f"\n🔍 Fetching package info from: {packages_url}")
        response = requests.get(packages_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            packages_info = response.json()
            result["packages"] = packages_info
            print(f"✅ Retrieved package information")
        else:
            print(f"ℹ️  Package endpoint not available or requires authentication (HTTP {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"ℹ️  Could not fetch package info: {e}")
    
    return result


def print_language_report(result: Dict):
    """Print a formatted report of the language support."""
    print("\n" + "=" * 70)
    print("LANGUAGE SUPPORT REPORT")
    print("=" * 70)
    
    if result["status"] == "error":
        print(f"\n❌ Error: {result['error']}")
        return
    
    print(f"\n🌐 API Server: {result['api_url']}")
    print(f"📊 Total Languages: {result['language_count']}")
    
    if result["languages"]:
        print("\n📋 Supported Languages:")
        print("-" * 70)
        
        # Sort by code
        languages_sorted = sorted(result["languages"], key=lambda x: x.get("code", ""))
        
        # Group by region (if we can identify)
        european_codes = {
            "en", "es", "fr", "de", "it", "pt", "ru", "pl", "nl", "el", "cs", "ro",
            "hu", "sv", "no", "nb", "da", "fi", "bg", "hr", "sr", "sk", "sl", "lt",
            "lv", "et", "ga", "ca", "uk", "be", "is", "mk", "sq"
        }
        
        european = []
        asian = []
        middle_eastern = []
        african = []
        other = []
        
        asian_codes = {"zh", "ja", "ko", "hi", "th", "vi", "id", "ms", "tl", "bn", "gu", "kn", "ml", "mr", "ta", "te", "si", "my", "km", "lo", "ne", "pa", "mn"}
        middle_eastern_codes = {"ar", "he", "fa", "tr", "az", "hy", "ka", "kk", "ky", "tg", "uz", "ps", "ur"}
        african_codes = {"sw", "af", "ha", "ig", "yo", "zu", "so", "am"}
        
        for lang in languages_sorted:
            code = lang.get("code", "")
            name = lang.get("name", code)
            
            if code in european_codes:
                european.append((code, name))
            elif code in asian_codes:
                asian.append((code, name))
            elif code in middle_eastern_codes:
                middle_eastern.append((code, name))
            elif code in african_codes:
                african.append((code, name))
            else:
                other.append((code, name))
        
        if european:
            print("\n🇪🇺 European Languages:")
            for code, name in sorted(european):
                print(f"   {code:6} - {name}")
        
        if asian:
            print("\n🇦🇸 Asian Languages:")
            for code, name in sorted(asian):
                print(f"   {code:6} - {name}")
        
        if middle_eastern:
            print("\n🌍 Middle Eastern & Central Asian Languages:")
            for code, name in sorted(middle_eastern):
                print(f"   {code:6} - {name}")
        
        if african:
            print("\n🌍 African Languages:")
            for code, name in sorted(african):
                print(f"   {code:6} - {name}")
        
        if other:
            print("\n🌐 Other Languages:")
            for code, name in sorted(other):
                print(f"   {code:6} - {name}")
        
        # Language codes list
        codes = [lang.get("code", "") for lang in languages_sorted]
        print("\n" + "-" * 70)
        print(f"Language Codes ({len(codes)}):")
        print(", ".join(codes))
    
    # Package information
    if result["packages"]:
        print("\n" + "=" * 70)
        print("PACKAGE INFORMATION")
        print("=" * 70)
        
        packages = result["packages"]
        if isinstance(packages, dict):
            installed = packages.get("installed_packages", [])
            total_pairs = packages.get("total_pairs", 0)
            unique_languages = packages.get("unique_languages", [])
            
            print(f"\n📦 Installed Packages: {len(installed)}")
            print(f"🔗 Total Language Pairs: {total_pairs}")
            print(f"🌍 Unique Languages: {len(unique_languages)}")
            
            if unique_languages:
                print(f"\nLanguages from packages: {', '.join(sorted(unique_languages))}")
    
    print("\n" + "=" * 70)


def main():
    """Main function."""
    import argparse
    import os
    
    parser = argparse.ArgumentParser(
        description="Check what languages the API server supports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check without API key (if API_KEY_REQUIRED=false)
  python check_api_languages.py
  
  # Check with API key
  python check_api_languages.py --api-key YOUR_API_KEY
  
  # Check different server
  python check_api_languages.py --api-url http://localhost:5000
  
  # Save results to file
  python check_api_languages.py --api-key YOUR_KEY --output languages.json
  
  # Use environment variable for API key
  export TRANSLATE_API_KEY=your-key
  python check_api_languages.py
        """
    )
    parser.add_argument(
        "--api-url",
        default=os.getenv("TRANSLATE_API_URL", "https://api.shravani.group"),
        help="Base URL of the API server (default: https://api.shravani.group or TRANSLATE_API_URL env var)"
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("TRANSLATE_API_KEY"),
        help="API key for authentication (optional, can also use TRANSLATE_API_KEY env var)"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output JSON file path (optional)"
    )
    
    args = parser.parse_args()
    
    # Check if requests is installed
    try:
        import requests
    except ImportError:
        print("❌ Error: 'requests' library is required.")
        print("   Install it with: pip install requests")
        sys.exit(1)
    
    # Warn if API key might be needed
    if not args.api_key:
        print("ℹ️  Note: API key not provided. If the server requires authentication,")
        print("   use --api-key YOUR_KEY or set TRANSLATE_API_KEY environment variable.")
        print()
    
    # Query API
    result = check_api_languages(args.api_url, args.api_key)
    
    # Print report
    print_language_report(result)
    
    # Save to JSON if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n✅ Results saved to: {args.output}")
    
    # Exit with appropriate code
    if result["status"] == "error":
        if "401" in str(result.get("error", "")) or "API key" in str(result.get("error", "")):
            print("\n💡 Tip: The API requires authentication. Provide an API key:")
            print("   python check_api_languages.py --api-key YOUR_API_KEY")
            print("   Or set: export TRANSLATE_API_KEY=your-key")
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

