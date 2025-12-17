# Build Fix for sentencepiece Compilation

## Issue
Build fails when compiling `sentencepiece` on ARM64 architecture during deployment.

## Solution Applied

Updated `nixpacks.toml` to include additional build dependencies:
- `make` - Build automation tool
- `ninja` - Fast build system
- `g++` - C++ compiler (required for sentencepiece)

## Updated Configuration

```toml
[phases.setup]
nixPkgs = ["python312", "python312Packages.pip", "cmake", "pkg-config", "gcc", "make", "ninja", "g++"]
```

## Why This Fixes It

`sentencepiece` is a C++ library that needs to be compiled from source on ARM64. It requires:
1. **cmake** - Build system generator
2. **gcc/g++** - C/C++ compilers
3. **make** - Build automation
4. **ninja** - Fast parallel build system
5. **pkg-config** - Dependency detection

## Next Steps

1. **Commit and push** the updated `nixpacks.toml`
2. **Redeploy** in Coolify
3. **Monitor build logs** - First build will take longer (~5-10 minutes)
4. **Verify** deployment completes successfully

## Expected Build Time

- **First build**: 5-10 minutes (compiles sentencepiece)
- **Subsequent builds**: 2-3 minutes (uses cached layers)

## Alternative Solutions

If build still fails, try:

### Option 1: Use Pre-built Wheel (if available)
Check if there's a pre-built wheel for your architecture:
```bash
pip install --only-binary sentencepiece sentencepiece
```

### Option 2: Increase Build Resources
In Coolify, check if you can increase:
- Build timeout
- Memory allocation
- CPU allocation

### Option 3: Use Dockerfile Instead
Switch to Dockerfile build method in Coolify settings, which has more control over the build environment.

## Verification

After successful deployment:
1. Check container logs for startup
2. Verify `/health` endpoint responds
3. Check that models can be installed
4. Test `/languages` endpoint

