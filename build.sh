#!/bin/bash

# Build script for creating executables for all platforms

echo "Building Backdrop-Off for all platforms..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
pip install pyinstaller

# Build executable
echo "Building executable..."
pyinstaller backdrop-off.spec

echo "Build complete! Check the 'dist' folder for your executable."
echo ""
echo "To run the executable:"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "  dist/Backdrop-Off.exe"
else
    echo "  ./dist/Backdrop-Off"
fi
