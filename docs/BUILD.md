# Building Voice Assistant .exe Files

## Quick Start

The hotkey has been changed from **Ctrl+M** to **Alt+R** throughout the application.

## Building the .exe Files

You have two options to build the executables:

### Option 1: Using Python Script (Recommended)
```bash
python build.py
```

### Option 2: Using Batch Script (Windows)
```bash
build.bat
```

Both scripts will:
1. Install PyInstaller if needed
2. Clean previous builds
3. Build two executables:
   - `dist/vokey_gui/vokey_gui.exe` - GUI version with interface
   - `dist/vokey_background/vokey_background.exe` - Background version with system tray

## Build Requirements

Make sure you have all dependencies installed:
```bash
pip install -r requirements.txt
```

## Running the Executables

After building:

### GUI Version
- Navigate to `dist/vokey_gui/`
- Double-click `vokey_gui.exe`
- The application will open with a graphical interface
- **Hotkey: Alt+R** to start/stop recording

### Background Version  
- Navigate to `dist/vokey_background/`
- Double-click `vokey_background.exe`
- No console window will appear
- A system tray icon will appear in your taskbar
- **Hotkey: Alt+R** to start/stop recording
- Right-click the tray icon to exit

## Distribution

The executables in the `dist` folder can be distributed to other Windows computers
without requiring Python installation. Each folder contains all necessary dependencies.

## Troubleshooting

If the build fails:
1. Make sure you're in the project directory
2. Activate the virtual environment: `venv\Scripts\activate`
3. Install all requirements: `pip install -r requirements.txt`
4. Try again

For runtime issues, check the log file `vokey_YYYYMMDD.log` in the same directory.
