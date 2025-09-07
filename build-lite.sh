#!/bin/bash

# Optimized build script for smaller executables

echo "Building optimized Backdrop-Off executable..."
echo "This may take several minutes..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv-lite" ]; then
    echo "Creating lightweight virtual environment..."
    python -m venv venv-lite
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv-lite/Scripts/activate
else
    source venv-lite/bin/activate
fi

# Install minimal dependencies
echo "Installing minimal dependencies..."
pip install --no-cache-dir -r requirements-lite.txt
pip install pyinstaller

# Check if UPX is available for compression
if command -v upx &> /dev/null; then
    echo "UPX found - will use compression"
    UPX_FLAG="--upx-dir=$(which upx | xargs dirname)"
else
    echo "UPX not found - skipping compression (install UPX for smaller files)"
    UPX_FLAG=""
fi

# Build optimized executable
echo "Building executable with size optimizations..."
pyinstaller \
    --onefile \
    --windowed \
    --name=Backdrop-Off-Lite \
    --hidden-import=customtkinter \
    --hidden-import=PIL._tkinter_finder \
    --hidden-import=PIL.Image \
    --hidden-import=rembg \
    --hidden-import=onnxruntime \
    --hidden-import=tkinter.colorchooser \
    --hidden-import=tkinter.filedialog \
    --hidden-import=tkinter.messagebox \
    --exclude-module=matplotlib \
    --exclude-module=scipy \
    --exclude-module=pandas \
    --exclude-module=jupyter \
    --exclude-module=notebook \
    --exclude-module=IPython \
    --exclude-module=pytest \
    --exclude-module=setuptools \
    --exclude-module=distutils \
    --exclude-module=unittest \
    --exclude-module=sqlite3 \
    --exclude-module=multiprocessing \
    --exclude-module=asyncio \
    --exclude-module=logging \
    --exclude-module=email \
    --exclude-module=html \
    --exclude-module=http \
    --exclude-module=xml \
    --strip \
    $UPX_FLAG \
    --noconfirm \
    --clean \
    bg_remover_ui.py

echo ""
echo "Build complete!"

# Show file sizes
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    if [ -f "dist/Backdrop-Off-Lite.exe" ]; then
        echo "Optimized executable size:"
        ls -lh dist/Backdrop-Off-Lite.exe
        echo ""
        echo "To run: dist/Backdrop-Off-Lite.exe"
    fi
else
    if [ -f "dist/Backdrop-Off-Lite" ]; then
        echo "Optimized executable size:"
        ls -lh dist/Backdrop-Off-Lite
        echo ""
        echo "To run: ./dist/Backdrop-Off-Lite"
    fi
fi

echo ""
echo "Size optimization tips applied:"
echo "✓ Excluded unnecessary modules"
echo "✓ CPU-only ONNX Runtime"
echo "✓ Minimal dependencies"
echo "✓ Stripped debug symbols"
if command -v upx &> /dev/null; then
    echo "✓ UPX compression enabled"
else
    echo "- UPX compression (install UPX for even smaller size)"
fi
