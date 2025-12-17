# How to Check API Server Language Support

## Quick Summary

Your API server is configured to support **86 languages** by default. To check the actual installed languages, you have several options:

## Option 1: Make `/languages` Endpoint Public (Recommended)

I've updated the code to make the `/languages` endpoint publicly accessible (no API key required). After you deploy the updated code, you can check languages without authentication.

**Changes made:**
- Created `verify_api_key_optional()` function for public endpoints
- Updated `/languages` endpoint to use optional authentication
- Languages endpoint is now always accessible, but still accepts API keys for usage tracking

**To apply:**
1. Deploy the updated `main.py` to your server
2. Restart the API server
3. Run: `python check_api_languages.py --api-url https://api.shravani.group`

## Option 2: Use API Key (Current Method)

If you have an API key configured:

```bash
# Using the script
python check_api_languages.py --api-url https://api.shravani.group --api-key YOUR_API_KEY

# Or using curl
curl -H "X-API-Key: YOUR_API_KEY" https://api.shravani.group/languages | jq 'length'
```

## Option 3: Check Server Logs

When the server starts, it logs the number of installed packages. Look for lines like:
```
Translation service initialized with X packages
Available languages: en, es, fr, ...
```

## Option 4: Query from Frontend

The frontend can also query the languages endpoint. Check the browser console when loading the translation page.

## Expected Results

### Default Configuration (INSTALL_ALL_LANGUAGES=false)
- **86 languages** configured
- **Hundreds to thousands of language pairs** (e.g., en→es, es→en, en→fr, etc.)

### Extended Configuration (INSTALL_ALL_LANGUAGES=true)
- **100+ languages** (all available Argos Translate models)
- **Thousands of language pairs**

## Files Created

1. **`check_api_languages.py`** - Script to query API and get language count
   - Usage: `python check_api_languages.py [--api-url URL] [--api-key KEY]`
   - Supports environment variables: `TRANSLATE_API_URL`, `TRANSLATE_API_KEY`

2. **`check_backend_languages.py`** - Script to check languages locally (requires argostranslate installed)

3. **`LANGUAGE_SUPPORT_SUMMARY.md`** - Complete list of configured languages

## Next Steps

1. **Deploy the updated code** to make `/languages` publicly accessible
2. **Run the check script** to get exact language count
3. **Review the summary** to see all configured languages

## Quick Commands

```bash
# Check without API key (after deployment)
python check_api_languages.py

# Check with API key (current)
python check_api_languages.py --api-key YOUR_KEY

# Save results to file
python check_api_languages.py --output languages.json

# Count languages with curl
curl https://api.shravani.group/languages | jq 'length'
```

## Troubleshooting

### "API key required" error
- The server hasn't been updated yet with the public `/languages` endpoint
- Use `--api-key` flag or wait for deployment

### "Connection refused" or timeout
- Check if the API server is running
- Verify the API URL is correct
- Check firewall/network settings

### Empty language list
- Models may not be installed yet
- Check server logs for installation status
- Set `UPDATE_MODELS=true` and restart server

