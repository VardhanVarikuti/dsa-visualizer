#!/bin/bash

echo "Building DSA Visualizer for macOS..."

# Clean previous builds
rm -rf dist/ build/ *.spec

# Build the executable
pyinstaller --onefile --windowed --name "DSA Visualizer" main.py

# Create distribution directory
mkdir -p "DSA Visualizer macOS"
cp "dist/DSA Visualizer" "DSA Visualizer macOS/"
cp README.md "DSA Visualizer macOS/"
cp USER_GUIDE.md "DSA Visualizer macOS/"
cp ALGORITHM_COMPLEXITY.md "DSA Visualizer macOS/"
cp DEVELOPER_GUIDE.md "DSA Visualizer macOS/"
cp LICENSE "DSA Visualizer macOS/"

# Create a simple launcher script
cat > "DSA Visualizer macOS/Launch DSA Visualizer.command" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
./DSA\ Visualizer
EOF

chmod +x "DSA Visualizer macOS/Launch DSA Visualizer.command"

# Create ZIP archive
zip -r "DSA Visualizer macOS.zip" "DSA Visualizer macOS/"

echo "✅ Build complete! Distribution package: DSA Visualizer macOS.zip"
echo "📁 Contents:"
ls -la "DSA Visualizer macOS/" 