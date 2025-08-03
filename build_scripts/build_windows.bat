@echo off
echo Building DSA Visualizer for Windows...

REM Clean previous builds
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

REM Build the executable
pyinstaller --onefile --windowed --name "DSA Visualizer" main.py

REM Create distribution directory
mkdir "DSA Visualizer Windows"
copy "dist\DSA Visualizer.exe" "DSA Visualizer Windows\"
copy README.md "DSA Visualizer Windows\"
copy USER_GUIDE.md "DSA Visualizer Windows\"
copy ALGORITHM_COMPLEXITY.md "DSA Visualizer Windows\"
copy DEVELOPER_GUIDE.md "DSA Visualizer Windows\"
copy LICENSE "DSA Visualizer Windows\"

REM Create a simple launcher script
echo @echo off > "DSA Visualizer Windows\Launch DSA Visualizer.bat"
echo cd /d "%%~dp0" >> "DSA Visualizer Windows\Launch DSA Visualizer.bat"
echo start "" "DSA Visualizer.exe" >> "DSA Visualizer Windows\Launch DSA Visualizer.bat"

REM Create ZIP archive (requires 7zip or similar)
echo Creating ZIP archive...
powershell Compress-Archive -Path "DSA Visualizer Windows" -DestinationPath "DSA Visualizer Windows.zip" -Force

echo ✅ Build complete! Distribution package: DSA Visualizer Windows.zip
echo 📁 Contents:
dir "DSA Visualizer Windows" 