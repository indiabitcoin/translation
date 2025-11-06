#!/usr/bin/env python3
"""
Generate secure API keys for the translation server.
Usage: python generate_api_key.py [number_of_keys]
"""

import secrets
import sys

def generate_api_key(length=32):
    """Generate a secure random API key."""
    return secrets.token_urlsafe(length)

def main():
    # Number of keys to generate (default: 1)
    num_keys = 1
    if len(sys.argv) > 1:
        try:
            num_keys = int(sys.argv[1])
        except ValueError:
            print("Error: Number of keys must be an integer")
            sys.exit(1)
    
    print("=" * 60)
    print("Secure API Key Generator")
    print("=" * 60)
    print()
    
    keys = []
    for i in range(num_keys):
        key = generate_api_key()
        keys.append(key)
        print(f"API Key {i+1}: {key}")
    
    print()
    print("=" * 60)
    print("Configuration Instructions")
    print("=" * 60)
    print()
    print("Add these to your environment variables:")
    print()
    print("API_KEY_REQUIRED=true")
    if len(keys) == 1:
        print(f"API_KEYS={keys[0]}")
    else:
        print(f"API_KEYS={','.join(keys)}")
    print()
    print("For Coolify:")
    print("1. Go to your application settings")
    print("2. Navigate to Environment Variables")
    print("3. Add the variables above")
    print("4. Restart your application")
    print()
    print("⚠️  Keep these keys secure! Never commit them to Git.")
    print()

if __name__ == "__main__":
    main()

