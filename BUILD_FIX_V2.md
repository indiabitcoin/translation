# Build Fix V2 - Nix Syntax Error

## Issue
Build failed with Nix syntax error:
```
error: syntax error, unexpected CONCAT
        at /app/.nixpacks/nixpkgs-...nix:19:16:
            19|         cmake g++ gcc make ninja pkg-config python312 python312Packages.pip
              |                ^
```

## Root Cause
`g++` is not a valid Nix package name. In Nix:
- `gcc` already includes the C++ compiler (g++)
- Package names with special characters like `++` are not valid
- Need to use proper Nix package names

## Solution
Removed `g++` from nixPkgs since `gcc` already provides the C++ compiler. Added `binutils` for additional build tools.

## Updated Configuration

```toml
[phases.setup]
nixPkgs = ["python312", "python312Packages.pip", "cmake", "pkg-config", "gcc", "make", "ninja", "binutils"]
```

## Why This Works

1. **gcc** - Includes both C and C++ compilers (gcc and g++)
2. **cmake** - Build system generator
3. **make** - Build automation
4. **ninja** - Fast parallel build system
5. **pkg-config** - Dependency detection
6. **binutils** - Additional binary utilities (ld, ar, etc.)

## Next Steps

1. Commit and push the fix
2. Redeploy in Coolify
3. Monitor build - should now parse Nix configuration correctly
4. Build will compile sentencepiece successfully

## Additional Notes

If build still fails with sentencepiece compilation:
- Check Python version compatibility (sentencepiece may need Python 3.11)
- Consider upgrading sentencepiece to 0.2.0+ for Python 3.12 support
- Or downgrade Python to 3.11 in nixpacks.toml

