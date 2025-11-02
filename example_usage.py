#!/usr/bin/env python3
"""
Example script demonstrating how to use the LibreTranslate API.
Make sure the server is running before executing this script.
"""

import requests
import json

# Server URL
BASE_URL = "http://localhost:5000"

def test_health():
    """Test the health check endpoint."""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200

def test_languages():
    """Test the languages endpoint."""
    print("Testing languages endpoint...")
    response = requests.get(f"{BASE_URL}/languages")
    print(f"Status: {response.status_code}")
    languages = response.json()
    print(f"Found {len(languages)} languages:")
    for lang in languages[:10]:  # Show first 10
        print(f"  - {lang['code']}: {lang['name']}")
    if len(languages) > 10:
        print(f"  ... and {len(languages) - 10} more")
    print()
    return response.status_code == 200

def test_translate():
    """Test the translate endpoint."""
    print("Testing translate endpoint...")
    payload = {
        "q": "Hello, world!",
        "source": "en",
        "target": "es",
        "format": "text"
    }
    response = requests.post(
        f"{BASE_URL}/translate",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Original: {payload['q']}")
        print(f"Translated: {result['translatedText']}\n")
    else:
        print(f"Error: {response.text}\n")
    return response.status_code == 200

def test_detect():
    """Test the language detection endpoint."""
    print("Testing detect endpoint...")
    payload = {
        "q": "Bonjour, comment allez-vous?"
    }
    response = requests.post(
        f"{BASE_URL}/detect",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Text: {payload['q']}")
        print(f"Detected language: {result['language']} (confidence: {result['confidence']})\n")
    else:
        print(f"Error: {response.text}\n")
    return response.status_code == 200

def test_translate_auto():
    """Test translation with auto-detection."""
    print("Testing translate with auto-detection...")
    payload = {
        "q": "Guten Tag!",
        "source": "auto",
        "target": "en",
        "format": "text"
    }
    response = requests.post(
        f"{BASE_URL}/translate",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Original: {payload['q']}")
        print(f"Translated: {result['translatedText']}\n")
    else:
        print(f"Error: {response.text}\n")
    return response.status_code == 200

if __name__ == "__main__":
    print("=" * 50)
    print("LibreTranslate API Test Script")
    print("=" * 50)
    print()
    
    try:
        # Run tests
        results = []
        results.append(("Health Check", test_health()))
        results.append(("Languages", test_languages()))
        results.append(("Translate", test_translate()))
        results.append(("Detect Language", test_detect()))
        results.append(("Auto Translate", test_translate_auto()))
        
        # Summary
        print("=" * 50)
        print("Test Summary")
        print("=" * 50)
        for test_name, passed in results:
            status = "✓ PASSED" if passed else "✗ FAILED"
            print(f"{test_name}: {status}")
        
        all_passed = all(result[1] for result in results)
        print()
        if all_passed:
            print("All tests passed! ✓")
        else:
            print("Some tests failed. Make sure the server is running and translation models are installed.")
    
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
        print("Make sure the server is running at http://localhost:5000")
    except Exception as e:
        print(f"Error: {e}")

