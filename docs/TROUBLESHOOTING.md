# Troubleshooting Guide

## Issue: Background Mode Not Working

### Step 1: Test Dependencies

Run the dependency checker:
```bash
python test_deps.py
```

This will show which dependencies are missing.

### Step 2: Install Missing Dependencies

If ANY dependencies are missing, run:
```bash
# Option A: Run the installer
install_new_deps.bat

# Option B: Manual installation
pip install pywin32 pystray pillow
```

**Important for pywin32:**
After installing pywin32, you may need to run:
```bash
python venv\Scripts\pywin32_postinstall.py -install
```

### Step 3: Test the Script

Try running in regular Python first (not pythonw):
```bash
python start_background.pyw
```

This will show any errors in the console.

### Common Issues & Solutions

#### ModuleNotFoundError: No module named 'win32api'
**Solution:**
```bash
pip install pywin32
python venv\Scripts\pywin32_postinstall.py -install
```

#### ModuleNotFoundError: No module named 'pystray'
**Solution:**
```bash
pip install pystray
```

#### ModuleNotFoundError: No module named 'PIL'
**Solution:**
```bash
pip install pillow
```

#### ImportError with cursor_tracker
**Solution:** Make sure you're running from the vokey directory:
```bash
cd "vokey"
python start_background.pyw
```

#### No error but nothing happens
**Solution:** The script is likely waiting for the Whisper model to load. This can take 30-60 seconds the first time. Be patient and watch for the system tray icon to appear.

### Step 4: Check for the System Tray Icon

After running `start_background.pyw`, look for a microphone icon in your system tray (bottom-right corner of Windows).

- If you see it ✅ It's working! Right-click for menu.
- If not ❌ Check the log file `vokey_YYYYMMDD.log` for errors.

### Step 5: View Logs

If the script runs but doesn't work:
```bash
# Check today's log
type vokey_20260202.log
```

Look for error messages in the log file.

### Alternative: Test in Console Mode First

Before trying background mode, make sure the basic app works:
```bash
python main.py
```

- Press Ctrl+M
- Speak something
- Press Ctrl+M again
- Check if it types

If console mode works but background doesn't, it's likely a dependency issue with `pystray` or `pywin32`.

###  Manual Testing Steps

1. **Open a NEW terminal** (the current one might be stuck)

2. **Navigate to the project:**
   ```bash
   cd "vokey"
   ```

3. **Activate virtual environment** (if using one):
   ```bash
   venv\Scripts\activate
   ```

4. **Test dependencies:**
   ```bash
   python test_deps.py
   ```

5. **Install missing ones:**
   ```bash
   pip install pywin32 pystray pillow
   ```

6. **Test the script:**
   ```bash
   python start_background.pyw
   ```

7. **Look for errors** - If you see any Import errors or ModuleNotFound errors, that's the problem!

### Quick Fix Commands

```bash
# All-in-one fix
cd "vokey"
pip install pywin32 pystray pillow --upgrade
python start_background.pyw
```

### If Nothing Works

Try the simple console version first:
```bash
python main.py
```

If that works, the cursor tracking and background features work, but the system tray might have an issue.
