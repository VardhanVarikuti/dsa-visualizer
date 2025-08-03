# 🪟 Windows App Build Guide

This guide explains how to create a Windows executable for DSA Visualizer.

## 🎯 Options for Building Windows App

### Option 1: Build on Windows Machine (Recommended)

**Requirements:**
- Windows 10/11 machine
- Python 3.8+ installed
- Internet connection for dependencies

**Steps:**
1. **Clone the repository:**
   ```cmd
   git clone https://github.com/VardhanVarikuti/dsa-visualizer.git
   cd dsa-visualizer
   ```

2. **Install dependencies:**
   ```cmd
   pip install pygame pyinstaller
   ```

3. **Build the executable:**
   ```cmd
   pyinstaller --onefile --windowed --name "DSA Visualizer" main.py
   ```

4. **Test the executable:**
   ```cmd
   dist\DSA Visualizer.exe
   ```

5. **Create distribution package:**
   ```cmd
   mkdir "DSA Visualizer Windows"
   copy "dist\DSA Visualizer.exe" "DSA Visualizer Windows\"
   copy README.md "DSA Visualizer Windows\"
   copy USER_GUIDE.md "DSA Visualizer Windows\"
   copy ALGORITHM_COMPLEXITY.md "DSA Visualizer Windows\"
   copy DEVELOPER_GUIDE.md "DSA Visualizer Windows\"
   copy LICENSE "DSA Visualizer Windows\"
   ```

### Option 2: Use Windows Virtual Machine

**If you don't have a Windows machine:**

1. **Install VirtualBox or VMware**
2. **Download Windows 10/11 ISO** (free from Microsoft)
3. **Create Windows VM** with 4GB RAM, 20GB storage
4. **Follow Option 1 steps** in the VM

### Option 3: Use Windows Subsystem for Linux (WSL)

**On Windows 10/11:**
```bash
# Install WSL
wsl --install

# In WSL, follow Linux build instructions
# But note: GUI apps may not work properly in WSL
```

### Option 4: Use GitHub Actions (Automated)

**Create `.github/workflows/build-windows.yml`:**
```yaml
name: Build Windows Executable

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install pygame pyinstaller
    
    - name: Build executable
      run: |
        pyinstaller --onefile --windowed --name "DSA Visualizer" main.py
    
    - name: Create distribution package
      run: |
        mkdir "DSA Visualizer Windows"
        copy "dist\DSA Visualizer.exe" "DSA Visualizer Windows\"
        copy README.md "DSA Visualizer Windows\"
        copy USER_GUIDE.md "DSA Visualizer Windows\"
        copy ALGORITHM_COMPLEXITY.md "DSA Visualizer Windows\"
        copy DEVELOPER_GUIDE.md "DSA Visualizer Windows\"
        copy LICENSE "DSA Visualizer Windows\"
    
    - name: Upload Windows executable
      uses: actions/upload-artifact@v2
      with:
        name: DSA-Visualizer-Windows
        path: DSA Visualizer Windows/
```

## 🔧 Troubleshooting Windows Build

### Common Issues:

#### 1. "pyinstaller not found"
```cmd
pip install pyinstaller
```

#### 2. "pygame not found"
```cmd
pip install pygame
```

#### 3. "Missing DLL"
- Install Visual C++ Redistributable
- Or use `--onedir` instead of `--onefile`

#### 4. "App won't start"
- Check Windows Defender settings
- Right-click → "Run as administrator"
- Check Windows Event Viewer for errors

#### 5. "Large file size"
```cmd
# Use UPX compression
pip install upx
pyinstaller --onefile --windowed --upx-dir=path/to/upx main.py
```

## 📦 Distribution Options

### 1. Manual Distribution
- Create ZIP file of the executable
- Share via email, cloud storage, etc.

### 2. GitHub Releases
- Upload to GitHub releases
- Automatic download tracking

### 3. Website Distribution
- Host on personal website
- Direct download links

### 4. Microsoft Store
- Package as MSIX
- Submit to Microsoft Store

## 🎯 Expected Results

**File Structure:**
```
DSA Visualizer Windows/
├── DSA Visualizer.exe          # Main executable (~25MB)
├── Launch DSA Visualizer.bat   # Easy launcher
├── README.md                   # Quick start
├── USER_GUIDE.md              # User guide
├── ALGORITHM_COMPLEXITY.md    # Algorithm reference
├── DEVELOPER_GUIDE.md         # Developer guide
└── LICENSE                     # MIT License
```

**User Experience:**
1. Download ZIP file
2. Extract to any folder
3. Double-click `DSA Visualizer.exe`
4. No Python/Pygame installation needed!

## 🚀 Quick Build Commands

**For experienced users:**
```cmd
# One-liner build
pip install pygame pyinstaller && pyinstaller --onefile --windowed --name "DSA Visualizer" main.py
```

**For testing:**
```cmd
# Build with console for debugging
pyinstaller --onefile --console --name "DSA Visualizer Debug" main.py
```

**For smaller size:**
```cmd
# Exclude unnecessary modules
pyinstaller --onefile --windowed --exclude-module matplotlib --exclude-module numpy main.py
```

## 📊 File Size Optimization

**Typical sizes:**
- **Basic build**: ~25MB
- **Optimized build**: ~20MB
- **With UPX compression**: ~15MB

**Optimization tips:**
1. Exclude unused modules
2. Use UPX compression
3. Remove debug symbols
4. Strip unnecessary libraries

---

**Ready to build your Windows app! 🪟**

Choose your preferred method and start building! 