# How to Add New Languages to Your API Server

## Problem

Even with `INSTALL_ALL_LANGUAGES=true` set, new languages aren't being installed because:
1. `UPDATE_MODELS` must also be `true` to trigger installation
2. The auto-install only runs when NO models exist
3. Since you already have 49 languages, it won't automatically install more

## Solutions

### Solution 1: Set Both Environment Variables (Recommended)

In Coolify, set **both** environment variables:

```
INSTALL_ALL_LANGUAGES=true
UPDATE_MODELS=true
```

Then **redeploy** the server. This will:
- Update the package index
- Install ALL available language pairs
- Add new languages to your existing 49

**Important**: After installation completes, you can set `UPDATE_MODELS=false` to speed up future startups.

### Solution 2: Use the New API Endpoint

I've added a new endpoint to trigger model installation:

```bash
# Install/update models (requires API key if API_KEY_REQUIRED=true)
curl -X POST https://api.shravani.group/admin/install-models?force=true \
  -H "X-API-Key: YOUR_API_KEY"
```

This will:
- Check for new available models
- Install missing language pairs
- Return updated language count

### Solution 3: Manual Installation Script

If you have SSH access to the server, you can run:

```bash
# SSH into your server
ssh your-server

# Navigate to app directory
cd /app

# Run installation script
python install_all_models.py --model-dir /app/models
```

## Step-by-Step: Add All Languages

### In Coolify Dashboard:

1. **Go to your application settings**
2. **Environment Variables** section
3. **Add/Update these variables:**
   ```
   INSTALL_ALL_LANGUAGES=true
   UPDATE_MODELS=true
   ```
4. **Save and Redeploy**
5. **Monitor logs** - You'll see:
   ```
   INSTALL_ALL_LANGUAGES=true: Installing all available language pairs...
   Installing X translation models...
   Downloading en -> xx...
   Successfully installed: en -> xx
   ```
6. **Wait for completion** - This can take 30-60 minutes depending on:
   - Number of models to install
   - Server bandwidth
   - Disk space

7. **After completion**, set:
   ```
   UPDATE_MODELS=false
   ```
   (This prevents re-installation on every restart)

8. **Verify** new languages:
   ```bash
   curl https://api.shravani.group/languages | jq 'length'
   ```

## Expected Results

After installation, you should have:
- **100+ languages** (instead of current 49)
- **Thousands of language pairs**
- Much larger model directory (5-10GB+)

## Troubleshooting

### Issue: Still only 49 languages after redeploy

**Check:**
1. Are both `INSTALL_ALL_LANGUAGES=true` AND `UPDATE_MODELS=true` set?
2. Check server logs for installation messages
3. Verify disk space is sufficient (need 5-10GB+)
4. Check if installation was interrupted

**Solution:**
- Use the API endpoint: `POST /admin/install-models?force=true`
- Or manually run `install_all_models.py` script

### Issue: Installation takes too long

**This is normal:**
- Each model is 50-500MB
- 100+ models = 5-10GB download
- Can take 30-60 minutes on first run

**Solution:**
- Be patient, monitor logs
- Installation happens in background
- Server remains available during installation

### Issue: Out of disk space

**Check:**
- Persistent volume size in Coolify
- Should be at least 10GB for all languages

**Solution:**
- Increase volume size in Coolify
- Or install only specific languages using `LOAD_ONLY`

## Quick Commands

```bash
# Check current language count
curl https://api.shravani.group/languages | jq 'length'

# Trigger model installation (if API endpoint available)
curl -X POST https://api.shravani.group/admin/install-models?force=true \
  -H "X-API-Key: YOUR_KEY"

# Check installed packages (requires API key)
curl -H "X-API-Key: YOUR_KEY" https://api.shravani.group/packages
```

## Next Steps

1. **Set environment variables** in Coolify
2. **Redeploy** the server
3. **Monitor logs** for installation progress
4. **Verify** new languages are available
5. **Set UPDATE_MODELS=false** after completion

---

**Current Status**: 49 languages  
**Target**: 100+ languages  
**Method**: Set `INSTALL_ALL_LANGUAGES=true` + `UPDATE_MODELS=true` and redeploy

