# Quick Fix: Build Error with Locked Files

## Problem
When running `python build.py`, you get:
```
PermissionError: [WinError 5] Access is denied: 'dist\vokey_gui\_internal\...'
```

## Cause
Some DLL files from the previous build are still locked (in use) by Windows.

## Solution

### Option 1: Use the Updated build.py (Recommended)
I've updated `build.py` to handle this error gracefully. Just run:
```bash
python build.py
```

The script will now skip locked files and continue building. PyInstaller will overwrite the necessary files.

### Option 2: Manual Cleanup First
If you want to ensure a completely clean build:

1. **Close all running vokey processes**:
   - Close any running `vokey_gui.exe`
   - Exit `vokey_background.exe` from system tray
   - Close any File Explorer windows viewing the `dist` folder

2. **Delete the dist folder**:
   ```bash
   rmdir /s /q dist
   ```

3. **Run the build**:
   ```bash
   python build.py
   ```

### Option 3: Use the Batch Script
The batch script handles this automatically:
```bash
build.bat
```

## Quick Test
To test your build after it completes:
```bash
dist\vokey_gui\vokey_gui.exe
```

Press **Alt+R** to test the new hotkey!
