# Live API Language Support - Current Status

**API Server**: https://api.shravani.group/  
**Last Checked**: December 17, 2025  
**Status**: ✅ Online and responding

## Total Languages: **49 languages**

## Language Breakdown

### 🇪🇺 European Languages (27)
- Bulgarian (bg)
- Catalan (ca)
- Czech (cs)
- Danish (da)
- German (de)
- Greek (el)
- English (en)
- Spanish (es)
- Estonian (et)
- Finnish (fi)
- French (fr)
- Irish (ga)
- Hungarian (hu)
- Italian (it)
- Lithuanian (lt)
- Latvian (lv)
- Norwegian Bokmål (nb)
- Dutch (nl)
- Polish (pl)
- Portuguese (pt)
- Romanian (ro)
- Russian (ru)
- Slovak (sk)
- Slovenian (sl)
- Albanian (sq)
- Swedish (sv)
- Ukrainian (uk)

### 🇦🇸 Asian Languages (10)
- Bengali (bn)
- Hindi (hi)
- Indonesian (id)
- Japanese (ja)
- Korean (ko)
- Malay (ms)
- Thai (th)
- Tagalog (tl)
- Vietnamese (vi)
- Chinese (zh)

### 🌍 Middle Eastern & Central Asian Languages (7)
- Arabic (ar)
- Azerbaijani (az)
- Persian (fa)
- Hebrew (he)
- Kyrgyz (ky)
- Turkish (tr)
- Urdu (ur)

### 🌐 Other Languages (5)
- Esperanto (eo)
- Basque (eu)
- Galician (gl)
- PB (pb) ⚠️ *Note: May be an error/placeholder*
- ZT (zt) ⚠️ *Note: May be an error/placeholder*

## Notes

1. **Two unusual entries**: `pb` (PB) and `zt` (ZT) appear in the language list. These may be:
   - Placeholder codes
   - Errors in model installation
   - Unknown language codes

2. **Language Pairs**: With 49 languages, you have **2,352 possible language pairs** (49 × 48), though not all pairs may have direct translation models installed.

3. **API Endpoint**: The `/languages` endpoint is now **publicly accessible** (no API key required) ✅

## Quick Check Commands

```bash
# Count languages
curl -s https://api.shravani.group/languages | jq 'length'

# List all language codes
curl -s https://api.shravani.group/languages | jq -r '.[].code' | sort

# Full detailed report
python check_api_languages.py --api-url https://api.shravani.group
```

## Comparison to Configuration

- **Configured in code**: 86 languages
- **Currently installed**: 49 languages
- **Coverage**: ~57% of configured languages

This suggests that either:
- Not all models were installed during deployment
- Some models failed to install
- `INSTALL_ALL_LANGUAGES` was set to `false` (default)

## Recommendations

1. **To add more languages**: Set `INSTALL_ALL_LANGUAGES=true` and redeploy
2. **To check package info**: Use the `/packages` endpoint (requires API key)
3. **To verify specific pairs**: Test translations between languages

---

**API Status**: ✅ Healthy  
**Languages Endpoint**: ✅ Public (no auth required)  
**Translation Endpoint**: Requires API key (if `API_KEY_REQUIRED=true`)
