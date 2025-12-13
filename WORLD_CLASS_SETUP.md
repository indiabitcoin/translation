# World-Class Translation Setup Guide

Quick guide to set up your translation server with maximum language coverage.

## Quick Start

### Step 1: Discover Available Models

```bash
python discover_all_models.py
```

This will:
- Show all available packages from Argos Translate
- Identify regional language availability
- Generate `model_discovery_report.json`
- Provide recommendations

### Step 2: Install All Official Models

**Option A: Using Environment Variable (Recommended for Docker/Coolify)**

Add to your environment variables:
```
INSTALL_ALL_LANGUAGES=true
UPDATE_MODELS=true
```

**Option B: Using Installation Script**

```bash
python install_all_models.py --model-dir /app/models
```

**Option C: Manual Installation**

```python
import argostranslate.package

argostranslate.package.update_package_index()
packages = argostranslate.package.get_available_packages()

for package in packages:
    try:
        download_path = package.download()
        argostranslate.package.install_from_path(download_path)
        print(f"Installed: {package.from_code} -> {package.to_code}")
    except Exception as e:
        print(f"Failed: {package.from_code} -> {package.to_code}: {e}")
```

### Step 3: Add Community Models

For regional languages not in the official index:

```bash
# Install Welsh model (example)
python install_community_model.py \
  --url "https://github.com/user/repo/releases/download/v1.0/en-cy.argosmodel" \
  --model-dir /app/models
```

See **[REGIONAL_LANGUAGES.md](REGIONAL_LANGUAGES.md)** for complete list of regional languages and sources.

### Step 4: Verify Installation

```bash
# Check installed packages
curl http://your-server:3000/packages

# Check available languages
curl http://your-server:3000/languages

# Test translation
curl -X POST http://your-server:3000/translate \
  -H "Content-Type: application/json" \
  -d '{"q": "Hello", "source": "en", "target": "es"}'
```

## Expected Results

After installation, you should have:
- **100+ language pairs** from official Argos Translate
- **50+ unique languages** supported
- **Regional language support** (where community models exist)
- **World-class coverage** for global translation needs

## Storage Requirements

- **Per model:** 50-500MB
- **100 models:** ~10-50GB
- **All models:** ~50-100GB (depending on language pairs)

Ensure you have sufficient storage in your persistent volume.

## Performance Considerations

- **Startup time:** Longer with more models (models load on-demand)
- **Memory usage:** Models are loaded into memory on first use
- **Translation speed:** 50-200ms per request (unchanged)

## Troubleshooting

### Models Not Installing

1. Check storage space: `df -h /app/models`
2. Check network connectivity
3. Review server logs for errors
4. Try installing models individually

### Models Not Detected

1. Verify symlink: `ls -la ~/.local/share/argos-translate/packages`
2. Check model directory: `ls -la /app/models`
3. Restart server after installation
4. Use `/packages` endpoint to verify

### Missing Regional Languages

1. Check `model_discovery_report.json` for availability
2. Search LibreTranslate Community Forum
3. Consider training custom models (see REGIONAL_LANGUAGES.md)

## Next Steps

1. **Review Discovery Report:** Check `model_discovery_report.json` for detailed analysis
2. **Add Community Models:** Install models for specific regional languages you need
3. **Monitor Usage:** Track which languages are actually used
4. **Optimize:** Remove unused models if storage is limited

## Resources

- **[REGIONAL_LANGUAGES.md](REGIONAL_LANGUAGES.md)** - Complete regional language guide
- **[COMMUNITY_MODELS.md](COMMUNITY_MODELS.md)** - Community model installation
- **[discover_all_models.py](discover_all_models.py)** - Model discovery script
- **[install_all_models.py](install_all_models.py)** - Bulk installation script

---

**Goal:** Achieve world-class translation coverage with maximum language support!

