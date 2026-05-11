#!/bin/bash
# Build Linux executable using PyInstaller
set -e

echo "=== Building DSA Visualizer for Linux ==="

# Install PyInstaller if needed
pip install pyinstaller

# Build the executable
pyinstaller --onefile \
    --name "dsa-visualizer" \
    --add-data "core:core" \
    --add-data "menus:menus" \
    --add-data "ui:ui" \
    --add-data "utils:utils" \
    --add-data "assets:assets" \
    main.py

echo ""
echo "Build complete! Executable is at: dist/dsa-visualizer"
echo "Run it with: ./dist/dsa-visualizer"
