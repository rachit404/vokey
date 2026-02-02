# 🎙️ Vokey - Voice Assistant

Voice to text assistant with hotkey activation (**Alt+R**).

Made completely with ***Google Antigravity IDE***

## ✨ Features

- 🎤 **Voice to text** using OpenAI Whisper (offline)
- ⌨️ **Hotkey activation**: Alt+R
- 🖥️ **Two versions**: GUI with history and background (system tray)
- 🔄 **Cross-application**: Works in any Windows app
- 📍 **Cursor tracking**: Types at original cursor position
- 🔊 **Audio feedback**: Beep sound on recording start
- ✨ **Visual feedback**: Cursor highlight on activation
- 💾 **History storage**: SQLite database with search and delete
- 🎨 **Custom icon**: Professional favicon integration

## 🚀 Quick Start

### Run from Source

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run GUI version (recommended)
python src/app.py

# Or run background version with system tray
pythonw src/start_background.pyw

# Or run CLI version
python src/main.py
```

### Run from Executable

1. Download the latest release from `dist/` folder
2. Run `vokey_gui.exe` for GUI version
3. Or run `vokey_background.exe` for system tray version
4. Press **Alt+R** to start recording in any application

## 📁 Project Structure

```
vokey/
├── src/                          # Source code
│   ├── app.py                   # GUI entry point (tkinter)
│   ├── main.py                  # CLI entry point
│   ├── start_background.pyw     # Background launcher (no console)
│   ├── core.py                  # Core functionality (recorder, transcriber, typer)
│   ├── cursor_tracker.py        # Cursor position tracking & feedback
│   ├── tray_icon.py             # System tray integration
│   └── ...
├── artifacts/                    # Assets and resources
│   ├── favicon_io/              # Icon files
│   │   └── favicon.ico          # Application icon (15KB)
│   └── ...
├── docs/                         # Documentation
│   ├── README.md                # Detailed documentation
│   ├── QUICKSTART.md            # Quick start guide
│   ├── BUILD.md                 # Build instructions
│   ├── TROUBLESHOOTING.md       # Common issues
│   └── ...
├── scripts/                      # Build and utility scripts
│   ├── build.py                 # Automated build script
│   ├── kill_processes.bat       # Kill Vokey processes (build helper)
│   ├── vokey_gui.spec           # PyInstaller config for GUI
│   ├── vokey_background.spec    # PyInstaller config for background
│   └── ...
├── dist/                         # Build output (.exe files)
│   ├── vokey_gui/               # GUI executable + dependencies
│   └── vokey_background/        # Background executable + dependencies
├── build/                        # PyInstaller build cache
├── requirements.txt              # Python dependencies
└── .gitignore
```

## 🔨 Building Executables

The build process is fully automated and includes automatic process cleanup:

```bash
# Build both GUI and background versions
python scripts/build.py
```

**What happens during build:**
1. ✅ Automatically kills any running Vokey processes
2. ✅ Cleans previous build artifacts
3. ✅ Builds GUI version with tkinter
4. ✅ Builds background version with system tray
5. ✅ Embeds favicon.ico as application icon
6. ✅ No manual confirmations needed (--noconfirm flag)

**Output files:**
- `dist/vokey_gui/vokey_gui.exe` - GUI version with history
- `dist/vokey_background/vokey_background.exe` - Background version with system tray

### Troubleshooting Build Errors

If you get **"Permission Denied"** errors during build:

```bash
# Manually kill Vokey processes
scripts\kill_processes.bat

# Wait a few seconds
timeout /t 3

# Try building again
python scripts/build.py
```

See [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) for more solutions.

## 📚 Documentation

- **[Full Documentation](docs/README.md)** - Complete feature guide
- **[Quick Start Guide](docs/QUICKSTART.md)** - Get started in 5 minutes
- **[Build Instructions](docs/BUILD.md)** - Detailed build process
- **[GitHub Release Guide](docs/GITHUB_RELEASE.md)** - How to publish releases
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and fixes

## 🎯 Usage

1. **Start the application** (GUI or background version)
2. **Position your cursor** where you want to type
3. **Press Alt+R** to start recording
4. **Speak your text**
5. **Press Alt+R again** to stop recording
6. Text will be typed at your cursor position automatically!

### GUI Version Features
- View transcription history
- Copy previous transcriptions
- Delete individual or all history items
- See recording duration and timestamps

### Background Version Features
- Runs silently in system tray
- Right-click tray icon for status and exit
- Minimal resource usage
- No visible window

## ⚙️ Requirements

- Windows 10/11
- Python 3.10+ (for running from source)
- Internet connection (first run only - to download Whisper model)

## 🔧 Dependencies

Main dependencies (see `requirements.txt` for full list):
- `openai-whisper` - Speech recognition
- `pyaudio` - Audio recording
- `keyboard` - Hotkey detection
- `pyautogui` - Cursor tracking and typing
- `pystray` - System tray integration
- `Pillow` - Icon handling
- `tkinter` - GUI (included with Python)

## 📝 License

This project was created entirely using Google Antigravity IDE.

## 🙏 Acknowledgments

- OpenAI Whisper for speech recognition
- Google Antigravity IDE for development assistance
