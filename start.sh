#!/bin/bash
# Startup script that installs models if needed and starts the server

set -e

echo "Starting LibreTranslate server..."

# Set model directory (persistent volume in Coolify)
MODEL_DIR="${ARGOS_TRANSLATE_PACKAGES:-/app/models}"

# Create model directory and link to expected location
mkdir -p "${MODEL_DIR}"
mkdir -p ~/.local/share/argos-translate

# Link model directory to expected location (if not already linked)
if [ ! -L ~/.local/share/argos-translate/packages ] && [ -d "${MODEL_DIR}" ]; then
    ln -sf "${MODEL_DIR}" ~/.local/share/argos-translate/packages
    echo "Linked model directory: ${MODEL_DIR} -> ~/.local/share/argos-translate/packages"
fi

# Install models if directory is empty or UPDATE_MODELS is true
if [ "${UPDATE_MODELS}" = "true" ] || [ -z "$(ls -A ${MODEL_DIR} 2>/dev/null)" ]; then
    echo "Installing/updating translation models..."
    echo "This may take several minutes on first run..."
    
    # Run Python script to install models
    python << EOF
import argostranslate.package
import sys

print("Updating package index...")
argostranslate.package.update_package_index()

print("Fetching available packages...")
available_packages = argostranslate.package.get_available_packages()
print(f"Found {len(available_packages)} available packages")

# Install packages
if "${LOAD_ONLY:-}" != "":
    languages = [lang.strip() for lang in "${LOAD_ONLY}".split(",")]
    print(f"Installing models for languages: {languages}")
    
    installed_count = 0
    for pkg in available_packages:
        if pkg.from_code in languages or pkg.to_code in languages:
            try:
                print(f"Installing {pkg.from_code} -> {pkg.to_code}...")
                argostranslate.package.install_from_path(pkg.download())
                installed_count += 1
            except Exception as e:
                print(f"Warning: Failed to install {pkg.from_code}->{pkg.to_code}: {e}")
    
    print(f"Installed {installed_count} packages")
else:
    print("Installing all available models (this may take a while)...")
    installed_count = 0
    for pkg in available_packages:
        try:
            print(f"Installing {pkg.from_code} -> {pkg.to_code}...")
            argostranslate.package.install_from_path(pkg.download())
            installed_count += 1
        except Exception as e:
            print(f"Warning: Failed to install {pkg.from_code}->{pkg.to_code}: {e}")
    
    print(f"Installed {installed_count} packages")

print("Model installation complete!")
EOF
else
    echo "Models already installed in ${MODEL_DIR}, skipping download..."
    echo "Set UPDATE_MODELS=true to update models"
fi

# Start the server
echo "Starting translation server..."
exec python main.py

