# Build Fix V3 - Correct Nix Package Names

## Issue
Build failed with error:
```
error: undefined variable 'make'
at ...nix:19:28:
    19|         binutils cmake gcc make ninja pkg-config ...
        |                            ^
```

## Root Cause
In Nix, package names are different from standard Linux package names:
- `make` → `gnumake` (GNU Make)
- `ninja` → `ninja-build` (Ninja build system)

## Solution
Updated `nixpacks.toml` to use correct Nix package names.

## Updated Configuration

```toml
[phases.setup]
nixPkgs = ["python312", "python312Packages.pip", "cmake", "pkg-config", "gcc", "gnumake", "ninja-build", "binutils"]
```

## Package Name Mappings

| Standard Name | Nix Package Name |
|--------------|------------------|
| `make` | `gnumake` |
| `ninja` | `ninja-build` |
| `g++` | Included in `gcc` |
| `gcc` | `gcc` ✓ |
| `cmake` | `cmake` ✓ |
| `pkg-config` | `pkg-config` ✓ |

## Why This Works

1. **gnumake** - GNU Make build tool (correct Nix package name)
2. **ninja-build** - Ninja build system (correct Nix package name)
3. **gcc** - Includes both C and C++ compilers
4. **cmake** - Build system generator
5. **pkg-config** - Dependency detection
6. **binutils** - Binary utilities

## Next Steps

1. Commit and push the fix
2. Redeploy in Coolify
3. Build should now install packages correctly
4. sentencepiece should compile successfully

## Notes

- Nix uses specific package names that may differ from standard Linux distributions
- Always use Nix package names in `nixpacks.toml`
- Check nixpkgs documentation for correct package names if needed

