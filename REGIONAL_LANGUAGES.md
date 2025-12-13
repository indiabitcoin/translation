# Regional Languages Support Guide

This guide provides comprehensive information about regional language support to make the translation service world-class.

## Overview

To achieve world-class translation coverage, we need to support:
- **Official Argos Translate models** (100+ language pairs)
- **Community-contributed models** (regional languages)
- **Custom trained models** (for specific needs)

## Discovering Available Models

### Method 1: Use Discovery Script

Run the discovery script to see all available models:

```bash
python discover_all_models.py
```

This will:
- List all available packages from Argos Translate
- Show which regional languages are available
- Generate a detailed report (`model_discovery_report.json`)
- Provide recommendations

### Method 2: Check Package Index Programmatically

```python
import argostranslate.package

# Update and fetch all packages
argostranslate.package.update_package_index()
packages = argostranslate.package.get_available_packages()

# Get all unique languages
languages = set()
for pkg in packages:
    languages.add(pkg.from_code)
    languages.add(pkg.to_code)

print(f"Total languages: {len(languages)}")
print(f"Languages: {sorted(languages)}")
```

## Installing All Available Models

### Option 1: Environment Variable (Recommended)

Set `INSTALL_ALL_LANGUAGES=true` in your environment:

```bash
export INSTALL_ALL_LANGUAGES=true
python main.py
```

### Option 2: Use Installation Script

```bash
# Install all models
python install_all_models.py --model-dir /app/models

# Dry run (see what would be installed)
python install_all_models.py --dry-run
```

### Option 3: Manual Installation

```python
import argostranslate.package

# Update package index
argostranslate.package.update_package_index()

# Get all packages
packages = argostranslate.package.get_available_packages()

# Install all
for package in packages:
    try:
        download_path = package.download()
        argostranslate.package.install_from_path(download_path)
        print(f"Installed: {package.from_code} -> {package.to_code}")
    except Exception as e:
        print(f"Failed {package.from_code} -> {package.to_code}: {e}")
```

## Regional Language Categories

### UK Regional Languages

| Language | Code | Status | Source |
|----------|------|--------|--------|
| Welsh | `cy` | ✅ Community Model | [LibreTranslate Forum](https://community.libretranslate.com/t/community-trained-welsh-model/994) |
| Scottish Gaelic | `gd` | ❌ Not Available | Requires custom training |
| Cornish | `kw` | ❌ Not Available | Requires custom training |
| Manx | `gv` | ❌ Not Available | Requires custom training |

**Installation:**
```bash
# Install Welsh model (if available)
python install_community_model.py --url <welsh_model_url> --model-dir /app/models
```

### European Regional Languages

| Language | Code | Status | Notes |
|----------|------|--------|-------|
| Breton | `br` | Check availability | Regional language of France |
| Occitan | `oc` | Check availability | Romance language |
| Corsican | `co` | Check availability | Regional language of France/Italy |
| Sardinian | `sc` | Check availability | Regional language of Italy |
| Romansh | `rm` | Check availability | Official language of Switzerland |
| Walloon | `wa` | Check availability | Regional language of Belgium |
| Friulian | `fur` | Check availability | Regional language of Italy |
| Ladino | `lad` | Check availability | Judeo-Spanish |

### African Languages

| Language | Code | Status | Notes |
|----------|------|--------|-------|
| Amharic | `am` | Check availability | Official language of Ethiopia |
| Fulah | `ff` | Check availability | West African language |
| Wolof | `wo` | Check availability | Senegal, Gambia |
| Xhosa | `xh` | ✅ Available | South Africa |
| Zulu | `zu` | ✅ Available | South Africa |
| Swahili | `sw` | ✅ Available | East Africa |

### Asian Regional Languages

| Language | Code | Status | Notes |
|----------|------|--------|-------|
| Assamese | `as` | Check availability | India |
| Odia | `or` | Check availability | India |
| Maithili | `mai` | Check availability | India, Nepal |
| Santali | `sat` | Check availability | India |
| Konkani | `kok` | Check availability | India |
| Manipuri | `mni` | Check availability | India |
| Bhojpuri | `bho` | Check availability | India |
| Rajasthani | `raj` | Check availability | India |
| Sindhi | `sd` | Check availability | Pakistan, India |
| Kashmiri | `ks` | Check availability | India, Pakistan |
| Dzongkha | `dz` | Check availability | Bhutan |
| Tibetan | `bo` | Check availability | Tibet, China |

### Indigenous Languages

| Language | Code | Status | Notes |
|----------|------|--------|-------|
| Quechua | `qu` | Check availability | South America |
| Aymara | `ay` | Check availability | South America |
| Guarani | `gn` | Check availability | South America |
| Inuktitut | `iu` | Check availability | Canada, Greenland |
| Ojibwe | `oj` | Check availability | North America |
| Cree | `cr` | Check availability | North America |
| Navajo | `nv` | Check availability | North America |
| Hawaiian | `haw` | Check availability | Hawaii |

## Finding Community Models

### 1. LibreTranslate Community Forum

**URL:** https://community.libretranslate.com/

Check for:
- Community model announcements
- Model quality feedback
- Download links
- Installation instructions

### 2. GitHub Search

Search for:
- `argosmodel` files
- `argos-translate` repositories
- Language-specific translation models

**Example searches:**
- `argosmodel welsh`
- `argos-translate community`
- `argosmodel regional language`

### 3. Argos Translate Package Index

**Repository:** https://github.com/argosopentech/argospm-index

This is the official package index. Check for:
- New language additions
- Community contributions
- Model metadata

## Model Installation Workflow

### Step 1: Discover Available Models

```bash
python discover_all_models.py
```

Review `model_discovery_report.json` to see:
- What's available
- What's missing
- Regional language coverage

### Step 2: Install Official Models

```bash
# Install all official models
export INSTALL_ALL_LANGUAGES=true
python main.py

# Or use the script
python install_all_models.py --model-dir /app/models
```

### Step 3: Install Community Models

For each community model:

```bash
# From URL
python install_community_model.py \
  --url "https://github.com/user/repo/releases/download/v1.0/en-cy.argosmodel" \
  --model-dir /app/models

# From local file
python install_community_model.py \
  --file ./en-cy.argosmodel \
  --model-dir /app/models
```

### Step 4: Verify Installation

```bash
# Check installed packages
curl http://localhost:3000/packages

# Check available languages
curl http://localhost:3000/languages

# Test translation
curl -X POST http://localhost:3000/translate \
  -H "Content-Type: application/json" \
  -d '{"q": "Hello", "source": "en", "target": "cy"}'
```

## Training Custom Models

For languages not available in official or community models:

### Using Argos Train

1. **Install Argos Train:**
   ```bash
   git clone https://github.com/argosopentech/argos-train
   cd argos-train
   pip install -r requirements.txt
   ```

2. **Prepare Training Data:**
   - Parallel corpus (source and target language pairs)
   - Minimum: 10,000 sentence pairs (more is better)
   - Format: TSV or TMX

3. **Train Model:**
   ```bash
   python train.py --source-lang en --target-lang gd --data-dir ./data
   ```

4. **Export Model:**
   ```bash
   python export.py --model-dir ./models/en-gd --output en-gd.argosmodel
   ```

5. **Install Model:**
   ```bash
   python install_community_model.py --file en-gd.argosmodel --model-dir /app/models
   ```

### Resources for Training Data

- **OPUS:** https://opus.nlpl.eu/ - Large collection of parallel corpora
- **Tatoeba:** https://tatoeba.org/ - Community-contributed sentence pairs
- **Common Crawl:** https://commoncrawl.org/ - Web crawl data
- **UN Parallel Corpus:** https://conferences.unite.un.org/UNCorpus

## Best Practices

### 1. Start with Official Models

Install all official Argos Translate models first:
```bash
export INSTALL_ALL_LANGUAGES=true
```

### 2. Add Community Models Selectively

Only install community models you actually need:
- Check model quality first
- Test with sample texts
- Verify license compatibility

### 3. Monitor Model Quality

- Test translations regularly
- Collect user feedback
- Compare with other translation services

### 4. Document Custom Models

If you train custom models:
- Document training data sources
- Record quality metrics
- Share with community (if allowed by license)

### 5. Regular Updates

- Update package index regularly
- Check for new community models
- Retrain custom models as needed

## Current Status

Run the discovery script to get current status:

```bash
python discover_all_models.py
```

This will show:
- Total available packages
- Installed packages
- Regional language availability
- Missing languages

## Resources

- **Argos Translate:** https://github.com/argosopentech/argos-translate
- **Package Index:** https://github.com/argosopentech/argospm-index
- **Argos Train:** https://github.com/argosopentech/argos-train
- **LibreTranslate Forum:** https://community.libretranslate.com/
- **OPUS Corpora:** https://opus.nlpl.eu/

## Contributing

If you have models for regional languages:

1. **Test thoroughly** with diverse text samples
2. **Share on forum:** Post to LibreTranslate Community
3. **Provide both directions:** Upload `lang1-lang2` and `lang2-lang1`
4. **Include documentation:** License, training data, quality metrics
5. **Update this guide:** Add your model to the appropriate section

---

**Last Updated:** December 2024  
**Maintained By:** Development Team

