# Build Issue Analysis - Why It Keeps Failing

## Root Cause

The build failures are happening because **Nixpacks is auto-generating Nix files** that reference packages in a way that doesn't work with the nixpkgs version being used. Each time we fix one package name, another fails.

## Pattern of Failures

1. **First**: `sentencepiece` compilation - needed build tools
2. **Second**: `g++` syntax error - not a valid Nix package name
3. **Third**: `make` undefined - needed to be `gnumake`
4. **Fourth**: `ninja-build` undefined - not a valid package name

## The Real Problem

Nixpacks generates a `.nix` file that tries to reference packages directly, but:
- Package names in Nix can vary by nixpkgs version
- The generated Nix file syntax may not match what's expected
- We're fighting against an auto-generated configuration

## Solutions

### Option 1: Use Dockerfile Instead (Recommended)

The repository already has a working `Dockerfile` that:
- Uses standard `apt-get` to install build dependencies
- Has proven build dependencies (cmake, gcc, etc.)
- More predictable and easier to debug

**To use Dockerfile in Coolify:**
1. Go to your Coolify application settings
2. Find "Build Pack" or "Build Method" option
3. Select "Dockerfile" instead of "Nixpacks"
4. Redeploy

### Option 2: Simplify nixpacks.toml

Remove all custom packages and let Nixpacks auto-detect, then install build tools via apt-get in the install phase:

```toml
[phases.setup]
nixPkgs = ["python312", "python312Packages.pip"]

[phases.install]
cmds = [
    "sudo apt-get update",
    "sudo apt-get install -y --no-install-recommends build-essential cmake pkg-config",
    "python3 -m venv /opt/venv",
    ". /opt/venv/bin/activate && pip install --no-cache-dir --upgrade pip setuptools wheel",
    ". /opt/venv/bin/activate && pip install --no-cache-dir -r requirements.txt"
]
```

### Option 3: Use Pre-built Wheels

If possible, use pre-built wheels for sentencepiece to avoid compilation entirely.

## Recommendation

**Use the Dockerfile approach** - it's more reliable, easier to debug, and already configured with the correct build dependencies.

