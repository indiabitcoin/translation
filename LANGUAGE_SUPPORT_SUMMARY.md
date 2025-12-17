# Language Support Summary

## API Server Language Support

Based on the code configuration, your API server supports the following languages:

### Default Configuration (INSTALL_ALL_LANGUAGES=false)

**Total: 86 languages** configured in the code

#### European Languages (32)
- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `it` - Italian
- `pt` - Portuguese
- `ru` - Russian
- `pl` - Polish
- `nl` - Dutch
- `el` - Greek
- `cs` - Czech
- `ro` - Romanian
- `hu` - Hungarian
- `sv` - Swedish
- `no` - Norwegian
- `nb` - Norwegian Bokmål
- `da` - Danish
- `fi` - Finnish
- `bg` - Bulgarian
- `hr` - Croatian
- `sr` - Serbian
- `sk` - Slovak
- `sl` - Slovenian
- `lt` - Lithuanian
- `lv` - Latvian
- `et` - Estonian
- `ga` - Irish
- `ca` - Catalan
- `uk` - Ukrainian
- `be` - Belarusian
- `is` - Icelandic
- `mk` - Macedonian
- `sq` - Albanian

#### Major World Languages (54)
- `zh` - Chinese
- `ja` - Japanese
- `ko` - Korean
- `ar` - Arabic
- `hi` - Hindi
- `tr` - Turkish
- `he` - Hebrew
- `th` - Thai
- `vi` - Vietnamese
- `id` - Indonesian
- `ms` - Malay
- `tl` - Tagalog
- `sw` - Swahili
- `af` - Afrikaans
- `az` - Azerbaijani
- `eu` - Basque
- `bn` - Bengali
- `bs` - Bosnian
- `br` - Breton
- `eo` - Esperanto
- `fa` - Persian
- `gl` - Galician
- `gu` - Gujarati
- `ha` - Hausa
- `haw` - Hawaiian
- `hy` - Armenian
- `ig` - Igbo
- `jw` - Javanese
- `ka` - Georgian
- `km` - Khmer
- `kn` - Kannada
- `kk` - Kazakh
- `ky` - Kyrgyz
- `lo` - Lao
- `lb` - Luxembourgish
- `ml` - Malayalam
- `mr` - Marathi
- `mn` - Mongolian
- `my` - Myanmar
- `ne` - Nepali
- `ps` - Pashto
- `pa` - Punjabi
- `si` - Sinhala
- `so` - Somali
- `su` - Sundanese
- `tg` - Tajik
- `ta` - Tamil
- `te` - Telugu
- `ur` - Urdu
- `uz` - Uzbek
- `yi` - Yiddish
- `yo` - Yoruba
- `zu` - Zulu

### Extended Configuration (INSTALL_ALL_LANGUAGES=true)

If `INSTALL_ALL_LANGUAGES=true` is set, the server will install **ALL available language pairs** from Argos Translate, which can be **100+ languages** depending on what's available in the Argos Translate package index.

## How to Check Actual Installed Languages

### Option 1: Query the API (Requires API Key)

```bash
# With API key
python check_api_languages.py --api-url https://api.shravani.group --api-key YOUR_API_KEY

# Save results to file
python check_api_languages.py --api-url https://api.shravani.group --api-key YOUR_API_KEY --output languages.json
```

### Option 2: Use curl

```bash
# Get languages list
curl -H "X-API-Key: YOUR_API_KEY" https://api.shravani.group/languages

# Get package information
curl -H "X-API-Key: YOUR_API_KEY" https://api.shravani.group/packages
```

### Option 3: Check Locally (if you have access to the server)

```bash
python check_backend_languages.py
```

## Language Pairs

The number of **language pairs** (translation directions) is much larger than the number of languages. For example:
- With 86 languages, you can have up to **86 × 85 = 7,310 possible pairs**
- However, Argos Translate may not have models for all pairs
- Typically, you'll have **hundreds to thousands of language pairs** installed

## Notes

1. **UK Regional Languages**: Welsh (cy), Scottish Gaelic (gd), Cornish (kw), and Manx (gv) are **not available** in default Argos Translate models. They require community-contributed models.

2. **Actual vs Configured**: The configured languages list shows what the server *tries* to install. The actual installed languages depend on:
   - What's available in Argos Translate package index
   - Which packages successfully downloaded and installed
   - Whether `INSTALL_ALL_LANGUAGES=true` is set

3. **To get the exact count**: Query the `/languages` endpoint or check the `/packages` endpoint for detailed information.

## Quick Check Commands

```bash
# Check health
curl https://api.shravani.group/health

# Check languages (requires API key if API_KEY_REQUIRED=true)
curl -H "X-API-Key: YOUR_KEY" https://api.shravani.group/languages | jq 'length'

# Count languages
curl -H "X-API-Key: YOUR_KEY" https://api.shravani.group/languages | jq '.[] | .code' | wc -l
```

