#!/bin/bash

# Build binary script for autodoc-cli

echo "🔨 Building autodoc binary..."

# Clean previous builds
rm -rf build/ dist/autodoc

# Build the binary
uv run pyinstaller --onefile --name autodoc autodoc/cli/main.py

# Check if build was successful
if [ -f "dist/autodoc" ]; then
    echo "✅ Binary built successfully!"
    echo "📁 Location: dist/autodoc"
    echo "📏 Size: $(du -h dist/autodoc | cut -f1)"
    
    # Test the binary
    echo "🧪 Testing binary..."
    ./dist/autodoc --help > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ Binary works correctly!"
    else
        echo "❌ Binary test failed!"
        exit 1
    fi
else
    echo "❌ Binary build failed!"
    exit 1
fi
