@echo off
REM Build Windows executable using PyInstaller
echo === Building DSA Visualizer for Windows ===

REM Install PyInstaller if needed
pip install pyinstaller

REM Build the executable
pyinstaller --onefile ^
    --name "DSA Visualizer" ^
    --windowed ^
    --add-data "core;core" ^
    --add-data "menus;menus" ^
    --add-data "ui;ui" ^
    --add-data "utils;utils" ^
    --add-data "assets;assets" ^
    main.py

echo.
echo Build complete! Executable is at: dist\DSA Visualizer.exe
pause