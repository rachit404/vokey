# Vokey - Voice Assistant

Voice to text assistant with hotkey activation (**Alt+R**).

Made completely with ***Google Antigravity IDE***

## Steps to Rebuild

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run GUI version
python src/app.py

#Or run CLI version
python src/main.py

# Build executables
python scripts/build.py
```

## Project Structure

```
vokey/
├── src/                    # Source code
│   ├── main.py            # CLI entry point
│   ├── app.py             # GUI entry point
│   ├── core.py            # Core functionality
│   └── ...
├── docs/                   # Documentation
│   ├── README.md          # Detailed documentation
│   ├── QUICKSTART.md      # Quick start guide
│   └── ...
├── scripts/                # Build and utility scripts
│   ├── build.py           # Build script
│   ├── *.spec             # PyInstaller configs
│   └── ...
├── dist/                   # Build output (.exe files)
├── requirements.txt        # Python dependencies
└── .gitignore
```

## Features

- **Voice to text** using OpenAI Whisper
- **Hotkey activation**: Alt+R
- **Two versions**: GUI and background (system tray)
- **Cross-application**: Works in any Windows app
- **Cursor tracking**: Types at original cursor position

## Documentation

See [`docs/README.md`](docs/README.md) for full documentation.

## Building

To create standalone .exe files:

```bash
python scripts/build.py
```

Output: `dist/vokey_gui/vokey_gui.exe` and `dist/vokey_background/vokey_background.exe`
