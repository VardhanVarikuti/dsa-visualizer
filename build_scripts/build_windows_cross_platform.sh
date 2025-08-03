#!/bin/bash

echo "Preparing Windows build from macOS..."

# Create Windows-specific requirements
cat > requirements_windows.txt << 'EOF'
pygame>=2.0.0
pyinstaller>=5.0.0
EOF

# Create Windows build spec
cat > DSA_Visualizer_Windows.spec << 'EOF'
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DSA Visualizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
EOF

# Create Windows distribution structure
mkdir -p "DSA Visualizer Windows"
cp README.md "DSA Visualizer Windows/"
cp USER_GUIDE.md "DSA Visualizer Windows/"
cp ALGORITHM_COMPLEXITY.md "DSA Visualizer Windows/"
cp DEVELOPER_GUIDE.md "DSA Visualizer Windows/"
cp LICENSE "DSA Visualizer Windows/"

# Create Windows launcher script
cat > "DSA Visualizer Windows/Launch DSA Visualizer.bat" << 'EOF'
@echo off
echo Starting DSA Visualizer...
start "" "DSA Visualizer.exe"
EOF

# Create build instructions for Windows
cat > "DSA Visualizer Windows/BUILD_INSTRUCTIONS.txt" << 'EOF'
WINDOWS BUILD INSTRUCTIONS
==========================

To build the Windows executable on a Windows machine:

1. Install Python 3.8+ from https://python.org
2. Install PyInstaller: pip install pyinstaller
3. Install Pygame: pip install pygame
4. Run: pyinstaller --onefile --windowed --name "DSA Visualizer" main.py
5. Copy the executable from dist/ to this folder
6. Test by running: DSA Visualizer.exe

The executable will be created in the dist/ folder.
EOF

echo "✅ Windows build preparation complete!"
echo "📁 Created: DSA Visualizer Windows/"
echo "📋 Next steps:"
echo "   1. Transfer this folder to a Windows machine"
echo "   2. Follow BUILD_INSTRUCTIONS.txt"
echo "   3. Copy the .exe file to this folder"
echo "   4. Create ZIP archive for distribution" 