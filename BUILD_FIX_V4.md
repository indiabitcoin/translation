# Build Fix V4 - Simplified Package List

## Issue
Build failed with error:
```
error: undefined variable 'ninja-build'
at ...nix:19:36:
    19|         binutils cmake gcc gnumake ninja-build pkg-config ...
        |                                    ^
```

## Root Cause
`ninja-build` is not a valid Nix package name in the nixpkgs version being used. Additionally, `ninja` is not strictly required for building `sentencepiece` - `cmake` and `make` are sufficient.

## Solution
Removed `ninja-build` from the package list. The essential build tools are:
- `gcc` - C/C++ compiler
- `cmake` - Build system
- `gnumake` - Build automation
- `pkg-config` - Dependency detection
- `binutils` - Binary utilities

## Updated Configuration

```toml
[phases.setup]
nixPkgs = ["python312", "python312Packages.pip", "cmake", "pkg-config", "gcc", "gnumake", "binutils"]
```

## Why This Works

1. **gcc** - Includes both C and C++ compilers (sufficient for sentencepiece)
2. **cmake** - Build system generator (required for sentencepiece)
3. **gnumake** - Build automation (required for sentencepiece)
4. **pkg-config** - Dependency detection
5. **binutils** - Binary utilities (ld, ar, etc.)

**Note**: `ninja` is optional - `cmake` can use `make` as the backend, which is sufficient.

## Next Steps

1. Commit and push the fix
2. Redeploy in Coolify
3. Build should now install packages correctly
4. sentencepiece should compile successfully with cmake + make

## Alternative Approach

If this still fails, we can try using the Dockerfile build method instead of Nixpacks, which gives more control over the build environment.

