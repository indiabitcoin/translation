# Community Models Guide

This guide explains how to install community-contributed translation models that are not included in the default Argos Translate package index.

**Official Argos Translate Repository**: [https://github.com/argosopentech/argos-translate](https://github.com/argosopentech/argos-translate)

The official package index (accessed via `argostranslate.package.get_available_packages()`) contains pre-trained models for many languages, but not all languages are included. Community-contributed models can extend support to additional languages.

## Available Community Models

### ✅ Welsh (cy) - Available

A community-trained Welsh model is available:
- **License**: MIT
- **Status**: Functional, tested by community
- **Source**: [LibreTranslate Community Forum - Welsh Model Thread](https://community.libretranslate.com/t/community-trained-welsh-model/994)
- **Note**: Check the forum thread for the latest download link (GitHub repository or direct download)

### ❌ Scottish Gaelic (gd) - Not Available

No community-contributed model exists yet. You would need to:
- Train a custom model using [Argos Train](https://github.com/argosopentech/argos-train)
- Or wait for community contributions

### ❌ Cornish (kw) - Not Available

No community-contributed model exists yet. You would need to:
- Train a custom model using [Argos Train](https://github.com/argosopentech/argos-train)
- Or wait for community contributions

## Installing Community Models

### Method 1: Manual Installation (Recommended)

1. **Download the `.argosmodel` file** from the community source (e.g., GitHub releases)

2. **Place the file** in your models directory:
   - **Local development**: `~/.local/share/argos-translate/packages/`
   - **Docker/Coolify**: `/app/models/` (or your `ARGOS_TRANSLATE_PACKAGES` directory)

3. **Restart the server** - Argos Translate will automatically detect and load the model

### Method 2: Using Python Script

You can use the provided `install_community_model.py` script:

```bash
# Install Welsh model from URL
python install_community_model.py \
  --url "https://github.com/user/repo/releases/download/v1.0/en-cy.argosmodel" \
  --model-dir /app/models

# Or install from local file
python install_community_model.py \
  --file ./en-cy.argosmodel \
  --model-dir /app/models
```

### Method 3: Programmatic Installation

You can install models programmatically in your code:

```python
import argostranslate.package
import urllib.request
import os

# Download model
model_url = "https://github.com/user/repo/releases/download/v1.0/en-cy.argosmodel"
model_path = "/tmp/en-cy.argosmodel"
urllib.request.urlretrieve(model_url, model_path)

# Install model
argostranslate.package.install_from_path(model_path)

# Clean up
os.remove(model_path)
```

## Finding Community Models

### LibreTranslate Community Forum

Check the [LibreTranslate Community Forum](https://community.libretranslate.com/) for:
- Announcements of new community models
- Model quality feedback
- Download links and installation instructions

### GitHub

Search GitHub for:
- `argosmodel` files
- `argos-translate` repositories
- Language-specific translation models

### Model Requirements

When installing community models, ensure:
- ✅ Model file has `.argosmodel` extension
- ✅ Model is compatible with your Argos Translate version
- ✅ You have both directions (e.g., `en-cy.argosmodel` AND `cy-en.argosmodel`) for full bidirectional support
- ✅ Model license allows your use case

## Verifying Installation

After installing a community model:

1. **Check installed packages**:
   ```python
   import argostranslate.package
   packages = argostranslate.package.get_installed_packages()
   for pkg in packages:
       if 'cy' in [pkg.from_code, pkg.to_code]:
           print(f"Found: {pkg.from_code} -> {pkg.to_code}")
   ```

2. **Test translation**:
   ```bash
   curl -X POST http://localhost:5000/translate \
     -H "Content-Type: application/json" \
     -d '{"q": "Hello", "source": "en", "target": "cy"}'
   ```

3. **Check languages endpoint**:
   ```bash
   curl http://localhost:5000/languages | grep -i welsh
   ```

## Troubleshooting

### Model Not Detected

- Ensure the model file is in the correct directory
- Check file permissions (must be readable)
- Verify the model file is not corrupted
- Restart the server after installation

### Translation Fails

- Verify you have both directions (e.g., `en-cy` and `cy-en`)
- Check model compatibility with Argos Translate version
- Review server logs for error messages

### Model Quality Issues

Community models may have varying quality:
- Test with sample texts before production use
- Consider training your own model if quality is insufficient
- Report issues to the model maintainer

## Contributing Models

If you train a model for an unsupported language:

1. **Train the model** using [Argos Train](https://github.com/argosopentech/argos-train)
2. **Test thoroughly** with diverse text samples
3. **Share on the forum**: Post to [LibreTranslate Community](https://community.libretranslate.com/)
4. **Provide both directions**: Upload both `lang1-lang2` and `lang2-lang1` models
5. **Include documentation**: License, training data source, quality metrics

## Official Package Index

The official Argos Translate package index is managed in the [argospm-index](https://github.com/argosopentech/argospm-index) repository. This index contains metadata and download links for all officially supported language pairs.

**To see what languages are officially supported:**
1. Check the [Argos Translate README](https://github.com/argosopentech/argos-translate#supported-languages)
2. Run `argostranslate.package.get_available_packages()` in Python
3. Browse the [package index repository](https://github.com/argosopentech/argospm-index)

**Requesting a language:** The Argos Translate project accepts language requests. If you need a language that's not in the official index, you can:
- Request it through the [LibreTranslate Community Forum](https://community.libretranslate.com/)
- Train and contribute a model yourself
- Use community-contributed models (like the Welsh model)

## Resources

- [Argos Translate Repository](https://github.com/argosopentech/argos-translate) - Main project repository
- [Argos Package Index](https://github.com/argosopentech/argospm-index) - Official package index
- [Argos Train](https://github.com/argosopentech/argos-train) - Training toolkit
- [Locomotive](https://github.com/LibreTranslate/Locomotive) - Model conversion tools
- [LibreTranslate Community Forum](https://community.libretranslate.com/) - Community discussions and model sharing

