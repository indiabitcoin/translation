# Coolify Deployment Troubleshooting

## Issue: Build Fails with "cmake: not found"

### Problem
The build fails because `sentencepiece` (a dependency of `argostranslate`) requires `cmake` to compile from source, especially on ARM64 architecture.

### Solution

The repository now includes:
1. **`nixpacks.toml`** - Configures Nixpacks to include cmake and other build dependencies
2. **Updated `Dockerfile`** - Includes cmake for direct Docker builds

### If Using Nixpacks (Default)

Coolify will automatically use the `nixpacks.toml` configuration which includes:
- `cmake` - Required for building sentencepiece
- `pkg-config` - Required for dependency detection
- `gcc` - C compiler

### Alternative: Force Dockerfile Usage

If you prefer to use the Dockerfile instead of Nixpacks:

1. In Coolify, go to your application settings
2. Look for "Build Pack" or "Build Method" option
3. Select "Dockerfile" instead of "Nixpacks"

The Dockerfile now includes:
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
```

### Environment Variables for Coolify

Make sure to set these in Coolify:

```
HOST=0.0.0.0
PORT=5000
UPDATE_MODELS=true              # Set to true on FIRST deployment only
LOAD_ONLY=en,es,fr,de          # Limit languages to reduce download time
ARGOS_TRANSLATE_PACKAGES=/app/models
```

### Persistent Volume

Add a persistent volume in Coolify:
- **Path:** `/app/models`
- **Size:** At least 2GB (more if installing many languages)

### If Build Still Fails

1. **Check build logs** - Look for specific missing dependencies
2. **Try installing dependencies manually** - Add to nixpacks.toml:
   ```toml
   [phases.setup]
   nixPkgs = ["python312", "cmake", "pkg-config", "gcc", "make", "ninja"]
   ```

3. **Use pre-built wheels** - Try pinning to a version with pre-built wheels:
   ```txt
   sentencepiece==0.1.99
   ```

### Common Issues

**Issue:** "Package sentencepiece was not found in the pkg-config search path"
- **Solution:** `pkg-config` is already in nixpacks.toml

**Issue:** "cmake: not found"
- **Solution:** `cmake` is already in nixpacks.toml

**Issue:** Build takes too long
- **Solution:** This is normal for first build. Subsequent builds are faster due to caching.

### Verifying the Fix

After deployment, check:
1. Build completes successfully
2. Container starts without errors
3. Models download correctly (check logs)
4. API responds at `/health` endpoint

### Notes

- The build will take longer on first deployment (~5-10 minutes) because it compiles `sentencepiece` from source
- ARM64 builds (like the error shows) require compilation, which is slower than x86_64
- Once built, the image is cached and subsequent deployments are faster

