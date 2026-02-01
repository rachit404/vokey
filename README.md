# 🎙️ Windows Voice-to-Text Assistant

A production-ready Windows voice assistant that converts voice to text using OpenAI Whisper and types it at your cursor position.

**Two versions available:**
- **CLI** (`main.py`): Lightweight background service with no UI
- **GUI** (`app.py`): Full application with history storage and management

## ✨ Features

- **Toggle recording**: Press `Ctrl + M` once to start, again to stop
- **Offline speech-to-text**: Uses OpenAI Whisper (no internet required)
- **Universal typing**: Works in ANY Windows application
- **Low latency**: Pre-loaded model for fast transcription
- **Background operation**: No UI, runs silently in the background
- **Keyboard simulation**: Types text character-by-character (no clipboard)

## 🔧 System Requirements

- **OS**: Windows 10/11
- **Python**: 3.10 or higher
- **Microphone**: Any working microphone device
- **RAM**: 2GB+ (for Whisper model)

## 📦 Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Installation

The first time you run the app, Whisper will download the model (~140MB for base model).

## 🚀 Usage

### Running the Assistant

```bash
python main.py
```

You should see:
```
📦 Loading Whisper model 'base'...
✅ Whisper model 'base' loaded successfully.

============================================================
🎙️  VOICE ASSISTANT STARTED
============================================================
Hotkey: CTRL+M
Press once to start recording.
Press again to stop recording and type text.
Press Ctrl+C to exit.
============================================================
```

### How to Use

1. Open any text editor (Notepad, Word, VS Code, browser, etc.)
2. Place your cursor where you want text to appear
3. **Press** `Ctrl + M` once to start recording
4. Speak your message
5. **Press** `Ctrl + M` again to stop
6. Wait 1-3 seconds for transcription
7. Text will be typed automatically at your cursor

### Example Workflow

```
1. Open Notepad
2. Click in the text area
3. Press Ctrl+M (recording starts)
4. Say: "Hello, this is a test"
5. Press Ctrl+M again (recording stops)
6. Text appears: Hello, this is a test
```

---

## 🖥️ GUI Application

### Running the GUI Version

```bash
python app.py
```

### GUI Features

- ✅ **Visual Interface**: Clean, modern tkinter interface
- ✅ **History Storage**: All transcriptions saved to SQLite database
- ✅ **History Management**: View, copy, and delete transcriptions
- ✅ **Real-time Status**: See recording/processing status
- ✅ **Hotkey Support**: Same Ctrl+M toggle works in GUI mode
- ✅ **Persistent Data**: History survives app restarts

### GUI Controls

**Main Window:**
- **Start Recording Button**: Click or press Ctrl+M to start/stop
- **Clear All Button**: Delete all history (with confirmation)
- **History Panel**: Scrollable list of all transcriptions

**Per-item Controls:**
- **Copy Button**: Copy text to clipboard
- **Delete Button**: Remove individual transcription

### Screenshot

```
┌─────────────────────────────────────────────────────┐
│  🎙️ Voice Assistant                    [ _ ] [□] [×] │
├─────────────────────────────────────────────────────┤
│  Status: Idle                    Hotkey: CTRL+M     │
├─────────────────────────────────────────────────────┤
│  [🎤 Start Recording]  [🗑️ Clear All]                │
├─────────────────────────────────────────────────────┤
│  📝 Transcription History (3 items)                 │
│  ┌───────────────────────────────────────────────┐ │
│  │ 2026-02-01 19:15  "Hello, this is a test"    │ │
│  │                   [📋 Copy] [🗑️ Delete]       │ │
│  │───────────────────────────────────────────────│ │
│  │ 2026-02-01 19:10  "Testing voice assistant"  │ │
│  │                   [📋 Copy] [🗑️ Delete]       │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

### Database Location

History is stored in `history.db` (SQLite) in the application directory:
```
vokey/
├── app.py
├── main.py
├── core.py
├── history.db  ← History database
└── requirements.txt
```

**Backup your history:**
```bash
copy history.db history_backup.db
```

---

## 🏗️ Building an Executable (.exe)

To create a standalone `.exe` that runs without Python installed:

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Build the Executable

```bash
pyinstaller --onefile --noconsole --name VoiceAssistant main.py
```

**Options explained:**
- `--onefile`: Packages everything into a single .exe
- `--noconsole`: Runs without a console window (background mode)
- `--name VoiceAssistant`: Names the output file `VoiceAssistant.exe`

### 3. Find Your Executable

The `.exe` will be located in:
```
dist\VoiceAssistant.exe
```

### 4. Running the Executable

**Important**: The first time you run the .exe, you need to run it from a command prompt to see the startup messages:

```bash
cd dist
VoiceAssistant.exe
```

After verification, you can:
- Add it to Windows startup
- Pin it to the taskbar
- Run it normally (it will run in background)

## ⚙️ Configuration

Edit `main.py` to customize:

```python
# Change the hotkey (line 284)
HOTKEY = "ctrl+m"  # Default

# Change the Whisper model (line 285)
WHISPER_MODEL = "base"   # Options: tiny, base, small, medium, large
```

### Supported Hotkey Formats

The `keyboard` library supports various key combinations:

**Single modifier + key:**
- `"ctrl+v"` - Ctrl + V
- `"alt+v"` - Alt + V  
- `"shift+v"` - Shift + V

**Multiple modifiers + key:**
- `"ctrl+shift+v"` - Ctrl + Shift + V
- `"ctrl+alt+v"` - Ctrl + Alt + V
- `"shift+alt+v"` - Shift + Alt + V
- `"ctrl+shift+alt+v"` - Ctrl + Shift + Alt + V

**Function keys:**
- `"f9"` - F9
- `"ctrl+f12"` - Ctrl + F12

**Special keys:**
- `"ctrl+space"` - Ctrl + Space
- `"alt+enter"` - Alt + Enter

> [!TIP]
> Choose a hotkey that doesn't conflict with other applications. `ctrl+alt+v` and `ctrl+shift+v` are good choices as they're rarely used by default Windows applications.


### Model Size Comparison

| Model  | Size | Speed | Accuracy |
|--------|------|-------|----------|
| tiny   | ~40MB | Fastest | Lower |
| **base** | ~140MB | **Fast** | **Good** (recommended) |
| small  | ~460MB | Medium | Better |
| medium | ~1.5GB | Slow | Very Good |
| large  | ~2.9GB | Slowest | Best |

## 🐛 Troubleshooting

### "No audio recorded"
- Check if your microphone is connected and working
- Try speaking louder or longer (minimum ~0.5 seconds)
- Verify microphone permissions in Windows Settings

### "Error starting recording"
- Ensure no other application is using the microphone
- Update your audio drivers
- Run `python -c "import sounddevice; print(sounddevice.query_devices())"` to check devices

### "Permission denied" when using hotkey
- Run the script as Administrator
- The `keyboard` library requires elevated permissions on some systems

### Text not typing
- Ensure the target application has focus (cursor is blinking)
- Check if the application allows programmatic input
- Try reducing typing speed in code (increase `typing_interval`)

### .exe doesn't work on another computer
- The target computer needs the Microsoft Visual C++ Redistributable
- Download: https://aka.ms/vs/17/release/vc_redist.x64.exe
- Or use `--onefile --add-binary` to include required DLLs

## 📝 Notes

- **First run**: Whisper model will be downloaded automatically (~140MB)
- **CPU usage**: Minimal when idle, spikes briefly during transcription
- **Privacy**: All processing is offline, no data leaves your computer
- **Security**: Uses only standard Windows APIs for keyboard simulation

## 🔒 Security Considerations

- Runs with user-level privileges only
- No network calls (fully offline after model download)
- Audio is discarded immediately after transcription
- No data persistence or logging

## 📄 License

MIT License - Feel free to modify and distribute

## 🤝 Contributing

Issues and pull requests welcome!

---

**Made with ❤️ for Windows productivity**