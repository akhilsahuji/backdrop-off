# Executable Size Optimization Guide

Your Backdrop-Off executable size can be significantly reduced with these optimization techniques.

## Current Size Issues

The standard build includes:
- **ONNX Runtime** (~200MB) - AI model runtime
- **rembg models** (~100MB) - Background removal models
- **Python standard library** (~50MB) - Full Python environment
- **CustomTkinter** (~20MB) - GUI framework
- **PIL/Pillow** (~10MB) - Image processing

**Total**: ~400-600MB executable

## Size Optimization Options

### Option 1: Optimized Build (Recommended)
Use the optimized build scripts provided:

**Windows:**
```bash
build-lite.bat
```

**macOS/Linux:**
```bash
./build-lite.sh
```

**Expected size reduction**: 30-50% smaller

### Option 2: Manual PyInstaller Optimizations

```bash
pyinstaller \
    --onefile \
    --windowed \
    --strip \
    --exclude-module=matplotlib \
    --exclude-module=scipy \
    --exclude-module=pandas \
    --exclude-module=jupyter \
    --exclude-module=setuptools \
    --exclude-module=unittest \
    --exclude-module=sqlite3 \
    --exclude-module=multiprocessing \
    --exclude-module=asyncio \
    --exclude-module=logging \
    bg_remover_ui.py
```

### Option 3: UPX Compression

Install UPX compressor for additional 30-50% size reduction:

**Windows:**
1. Download UPX from https://upx.github.io/
2. Add to PATH
3. Use `build-lite.bat`

**macOS:**
```bash
brew install upx
./build-lite.sh
```

**Linux:**
```bash
sudo apt-get install upx-ucl
./build-lite.sh
```

## Alternative Approaches

### 1. Two-Part Distribution
- **Lightweight installer** (~50MB) that downloads models on first run
- **Separate model package** (~300MB) downloaded automatically
- **Benefits**: Much smaller initial download, cached models

### 2. Web-Based Version
- **Electron app** (~100MB) with web interface
- **Server-side processing** using your existing Python code
- **Benefits**: Always up-to-date, smaller download

### 3. PyInstaller Directory Mode
Instead of `--onefile`, use directory distribution:
```bash
pyinstaller --windowed bg_remover_ui.py
```
- **Benefits**: Faster startup, smaller total size
- **Drawbacks**: Multiple files to distribute

## Size Comparison

| Build Type | Windows | macOS | Linux |
|------------|---------|-------|--------|
| Standard   | ~600MB  | ~550MB| ~500MB |
| Optimized  | ~400MB  | ~350MB| ~300MB |
| UPX + Opt  | ~250MB  | ~200MB| ~180MB |

## Trade-offs

### Optimized Builds
✅ **Pros:**
- Significantly smaller file size
- Faster download and distribution
- Excludes unnecessary dependencies

❌ **Cons:**
- Slightly longer build time
- May exclude some edge-case functionality

### UPX Compression
✅ **Pros:**
- Excellent compression ratios
- No functionality loss
- Transparent to end users

❌ **Cons:**
- Slower startup time (decompression)
- Some antivirus false positives
- Not available on all systems

## Recommended Workflow

1. **Development**: Use standard build for testing
2. **Release**: Use optimized build with UPX
3. **Distribution**: Provide both optimized and standard versions

## Implementation

The repository now includes:
- `requirements-lite.txt` - Minimal dependencies
- `build-lite.sh` - Optimized Unix build script
- `build-lite.bat` - Optimized Windows build script
- `optimized.spec` - PyInstaller spec with exclusions

Choose the optimization level that best fits your distribution needs!
