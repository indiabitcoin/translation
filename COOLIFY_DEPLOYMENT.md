# Deploying to Coolify

This guide explains how to deploy the LibreTranslate server to Coolify while staying within the 500MB repository limit.

## Strategy: Runtime Model Installation

**Key Point:** Translation models are NOT bundled in the Docker image. Instead, they are:
1. Downloaded at runtime when the container first starts
2. Stored in a persistent volume (survives container restarts)
3. Reused on subsequent deployments

This keeps your repository/build size small (< 50MB) while allowing unlimited model storage on the server.

## Deployment Steps

### 1. Prepare Your Repository

Your repository should be under 500MB (it will be, since we exclude models). Current structure:
```
LibreTranslate/
├── app/
├── main.py
├── requirements.txt
├── Dockerfile
├── start.sh          # Handles model installation
└── ...
```

**Size:** ~10-50MB (code only, no models)

### 2. Configure Coolify Deployment

#### Environment Variables

In Coolify, set these environment variables:

```
HOST=0.0.0.0
PORT=5000
UPDATE_MODELS=true              # Set to true on FIRST deployment
LOAD_ONLY=en,es,fr,de           # Languages you want (comma-separated)
API_KEY_REQUIRED=false          # Set to true for production
API_KEYS=key1,key2              # If API_KEY_REQUIRED=true
CORS_ORIGINS=*                  # Or specific domains
ARGOS_TRANSLATE_PACKAGES=/app/models
```

**Important Notes:**
- `UPDATE_MODELS=true` only needed on first run (downloads models)
- Set `LOAD_ONLY` to limit which languages to install (saves space/time)
- After first deployment, set `UPDATE_MODELS=false` for faster startups

#### Persistent Volume Configuration

In Coolify's volume settings:
- **Mount Path:** `/app/models`
- **Purpose:** Store translation models (persists between deployments)

This volume will:
- Preserve models when container restarts
- Speed up subsequent deployments (no re-download needed)
- Allow models to grow beyond container limits

### 3. Model Storage Considerations

**Model Sizes:**
- Each language pair: ~50-500MB
- Example: `en↔es`, `en↔fr`, `en↔de` ≈ 300-1500MB total
- All languages: ~5-10GB

**Recommendation:**
- Start with 2-5 languages you actually need
- Use `LOAD_ONLY` to limit installation
- Add more languages later by updating `LOAD_ONLY` and setting `UPDATE_MODELS=true`

### 4. First Deployment Workflow

1. **Push code to GitHub** (should be < 500MB ✓)

2. **Connect Coolify to your repository**

3. **Configure environment variables:**
   ```
   UPDATE_MODELS=true
   LOAD_ONLY=en,es,fr
   ```

4. **Add persistent volume:**
   - Path: `/app/models`
   - Size: At least 2GB (more if installing many languages)

5. **Deploy** - First deployment will:
   - Build small Docker image (~200MB)
   - Download models at runtime (~300-500MB per language pair)
   - Store models in persistent volume

6. **Subsequent deployments:**
   - Set `UPDATE_MODELS=false`
   - Models are reused from volume
   - Much faster startup (no download)

### 5. Optimizing Build Size

The Dockerfile is already optimized:
- ✅ Uses `python:3.10-slim` (smaller base image)
- ✅ Removes apt cache after installation
- ✅ Uses `--no-cache-dir` for pip
- ✅ No models in image

**Current build size:** ~150-250MB (just Python + dependencies)

### 6. Monitoring Model Installation

During first startup, check logs:
```bash
# In Coolify logs, you should see:
Installing/updating translation models...
Installing models for languages: en, es, fr
Model installation complete!
```

If installation fails:
- Check available disk space in Coolify
- Verify network connectivity
- Check `LOAD_ONLY` format (comma-separated, no spaces)

### 7. Updating Models

To add more languages later:

1. Update environment variable:
   ```
   LOAD_ONLY=en,es,fr,de,it,pt  # Added de, it, pt
   UPDATE_MODELS=true            # Download new ones
   ```

2. Redeploy - New models will be downloaded and added to existing ones

3. After successful deployment, set:
   ```
   UPDATE_MODELS=false           # Don't re-download on next deploy
   ```

### 8. Troubleshooting

**Problem: Build fails with size error**
- ✅ Models aren't in the repo (check `.gitignore`)
- ✅ Verify repository size is < 500MB

**Problem: Models not persisting**
- ✅ Verify persistent volume is mounted at `/app/models`
- ✅ Check volume permissions in Coolify

**Problem: Slow first startup**
- ✅ Normal - models downloading (can take 5-30 minutes)
- ✅ Use `LOAD_ONLY` to reduce download size
- ✅ Check network speed in Coolify

**Problem: Out of disk space**
- ✅ Reduce `LOAD_ONLY` to fewer languages
- ✅ Increase volume size in Coolify
- ✅ Check actual disk usage

## Example Coolify Configuration

### Environment Variables
```
HOST=0.0.0.0
PORT=5000
UPDATE_MODELS=false
LOAD_ONLY=en,es,fr,de
API_KEY_REQUIRED=true
API_KEYS=your-secret-key-here
CORS_ORIGINS=https://yourdomain.com
ARGOS_TRANSLATE_PACKAGES=/app/models
```

### Persistent Volume
```
Path: /app/models
Size: 5GB (or more if needed)
```

### Resource Limits
```
CPU: 1-2 cores
RAM: 1-2GB (models load into memory)
Disk: 5-10GB (for models)
```

## Cost & Storage Optimization

**Minimal Setup (3 languages):**
- Repository: ~20MB ✓
- Docker image: ~200MB ✓
- Models on server: ~500MB-1GB
- Total first deploy: < 500MB ✓

**Full Setup (all languages):**
- Repository: ~20MB ✓
- Docker image: ~200MB ✓
- Models on server: ~5-10GB (stored in persistent volume)
- Total first deploy: < 500MB ✓

**Key:** Models count toward server storage, NOT repository size!

## Summary

✅ **Repository stays small** - No models in code  
✅ **Models download at runtime** - On first container start  
✅ **Persistent volume** - Models survive restarts  
✅ **Selective installation** - Use `LOAD_ONLY` for needed languages  
✅ **Efficient updates** - Only download new models when `UPDATE_MODELS=true`

This approach lets you deploy to Coolify with a 500MB limit while still having access to all translation models!

