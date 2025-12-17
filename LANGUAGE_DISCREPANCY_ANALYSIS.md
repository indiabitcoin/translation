# Language Count Discrepancy Analysis

## Problem

**Deployment logs show:**
- ✅ 98 translation packages installed successfully
- ✅ Installation completed without errors

**But API shows:**
- ⚠️ Only 49 languages available
- ⚠️ Same count as before installation

## Analysis

### What the Logs Show

1. **98 packages installed** - All successful
2. **Installation completed** - Server started successfully
3. **Log shows**: "Available languages: ar, bn, ca, en, et, he, hu, it, ky, nb, pl, pt, ro, ru, sk, tl, tr, uk" (only 18 listed, but this is truncated)

### Possible Causes

#### 1. Server Not Restarted After Installation
- Packages were installed during startup
- But the language list might have been cached or generated before all packages were fully registered
- **Solution**: Restart the server

#### 2. Language Detection Issue
- The `get_languages()` method might not be detecting all languages from installed packages
- Some packages might not be properly registered
- **Solution**: Check the language detection logic

#### 3. Package Registration Delay
- Packages installed but not immediately available
- Argos Translate might need time to index new packages
- **Solution**: Wait and check again, or restart

#### 4. Unusual Language Codes
- `pb` and `zt` are present but might be causing issues
- These might be test/placeholder models
- **Solution**: Filter out invalid language codes

## Investigation Steps

### Step 1: Check Package Count via API

```bash
# Requires API key
curl -H "X-API-Key: YOUR_KEY" https://api.shravani.group/packages
```

This will show:
- Total installed packages
- Which language pairs are installed
- Model directory status

### Step 2: Restart Server

The server might need a restart to:
- Re-index installed packages
- Update language list
- Clear any caches

### Step 3: Check Server Logs

Look for:
- Language initialization messages
- Package loading errors
- Language detection warnings

## Expected Behavior

With 98 packages installed, you should have:
- **~30-50 unique languages** (depending on which pairs were installed)
- Most packages are bidirectional (en↔xx), so unique languages = packages / 2 + some non-English pairs

## Recommendations

1. **Restart the server** - This will re-initialize and detect all installed packages
2. **Check `/packages` endpoint** - Verify all 98 packages are detected
3. **Wait a few minutes** - Sometimes there's a delay in package registration
4. **Check for errors** - Look for any warnings in server logs about package loading

## Next Actions

1. Restart the server in Coolify
2. Wait 2-3 minutes after restart
3. Check language count again: `curl https://api.shravani.group/languages | jq 'length'`
4. If still 49, check `/packages` endpoint for detailed info

---

**Status**: Investigation needed  
**Issue**: 98 packages installed but only 49 languages detected  
**Action**: Restart server and re-check

