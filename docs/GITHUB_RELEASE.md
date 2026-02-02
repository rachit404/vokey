# 🚀 GitHub Release Guide

This guide walks you through creating a release on GitHub for the Vokey Voice Assistant project.

## 📋 Pre-Release Checklist

- [ ] All code changes committed and pushed
- [ ] README.md updated with latest features
- [ ] Version numbers updated (if applicable)
- [ ] Tests passed and application verified
- [ ] Build script tested successfully

---

## Step 1: Build the Executables

First, ensure you have clean, fresh builds of both versions:

```bash
cd "vokey"

# Make sure all processes are stopped
scripts\kill_processes.bat

# Build both versions
python scripts\build.py
```

**This creates:**
- `dist/vokey_gui/` - GUI version folder with all dependencies
- `dist/vokey_background/` - Background version folder with all dependencies

---

## Step 2: Create Release ZIP Files

Package the built executables for distribution:

### Using PowerShell

```powershell
# Navigate to dist folder
cd dist

# Create ZIP for GUI version
Compress-Archive -Path vokey_gui -DestinationPath vokey_gui_v1.0.0.zip -Force

# Create ZIP for background version
Compress-Archive -Path vokey_background -DestinationPath vokey_background_v1.0.0.zip -Force
```

### Using Command Prompt with tar (Windows 10+)

```bash
cd dist
tar -a -c -f vokey_gui_v1.0.0.zip vokey_gui
tar -a -c -f vokey_background_v1.0.0.zip vokey_background
```

> **Note:** Replace `v1.0.0` with your actual version number.

---

## Step 3: Commit and Push Your Code

Ensure all changes are committed to GitHub:

```bash
cd "vokey"

# Check status
git status

# Add all changes
git add .

# Commit with a descriptive message
git commit -m "Release v1.0.0: Icon integration and improved build process"

# Push to GitHub
git push origin main
```

---

## Step 4: Create GitHub Release

### Option A: Using GitHub Web Interface ⭐ (Recommended)

#### 4.1 Navigate to Releases

1. Go to your repository: `https://github.com/rachit404/vokey`
2. Click **"Releases"** in the right sidebar
3. Click **"Create a new release"** or **"Draft a new release"**

#### 4.2 Tag the Release

1. Click **"Choose a tag"**
2. Type your version number: `v1.0.0`
3. Click **"Create new tag: v1.0.0 on publish"**

#### 4.3 Set Release Title

```
Vokey v1.0.0 - Voice Assistant with Icon Integration
```

#### 4.4 Add Release Notes

Copy and customize this template:

```markdown
## 🎙️ Vokey v1.0.0 - Voice Assistant

Voice to text assistant with hotkey activation (Alt+R).

### ✨ Features
- 🎤 Voice to text using OpenAI Whisper (offline)
- ⌨️ Hotkey activation: Alt+R
- 🖥️ Two versions: GUI with history and background (system tray)
- 📍 Cursor tracking: Types at original cursor position
- 🔊 Audio & visual feedback on recording
- 💾 SQLite history storage
- 🎨 Professional favicon integration

### 📦 Downloads

**GUI Version** - Recommended for most users
- Download `vokey_gui_v1.0.0.zip`
- Extract and run `vokey_gui.exe`
- Features transcription history and management

**Background Version** - For minimal UI
- Download `vokey_background_v1.0.0.zip`
- Extract and run `vokey_background.exe`
- Runs silently in system tray

### 🚀 Quick Start
1. Download your preferred version
2. Extract the ZIP file
3. Run the `.exe` file
4. Press **Alt+R** to start recording in any application
5. Speak your text
6. Press **Alt+R** again to stop

### ⚙️ Requirements
- Windows 10/11
- Internet connection (first run only - downloads Whisper model ~140MB)

### 🐛 Known Issues
- First launch may take 30-60 seconds to download AI model
- Requires microphone permissions

### 📝 Changelog
- ✅ Added favicon.ico integration for professional appearance
- ✅ Improved build process with automatic process cleanup
- ✅ Fixed permission denied errors during builds
- ✅ Enhanced GUI with better icon display
- ✅ System tray icon now uses custom favicon
```

#### 4.5 Upload ZIP Files

1. Scroll to **"Attach binaries by dropping them here or selecting them"**
2. Drag and drop both ZIP files:
   - `vokey_gui_v1.0.0.zip`
   - `vokey_background_v1.0.0.zip`
3. Wait for upload to complete

#### 4.6 Publish

1. Check ✅ **"Set as the latest release"** (for main releases)
2. Click **"Publish release"**

---

### Option B: Using GitHub CLI

Install GitHub CLI from: https://cli.github.com/

```bash
# Login to GitHub (first time only)
gh auth login

# Create the release with files
gh release create v1.0.0 ^
  dist/vokey_gui_v1.0.0.zip ^
  dist/vokey_background_v1.0.0.zip ^
  --title "Vokey v1.0.0 - Voice Assistant with Icon Integration" ^
  --notes-file release_notes.md ^
  --latest

# Or with inline notes
gh release create v1.0.0 ^
  dist/vokey_gui_v1.0.0.zip ^
  dist/vokey_background_v1.0.0.zip ^
  --title "Vokey v1.0.0" ^
  --notes "Voice to text assistant with hotkey activation. See README for details." ^
  --latest
```

---

## Step 5: Verify the Release

1. Navigate to `https://github.com/rachit404/vokey/releases`
2. Verify your release has:
   - ✅ Correct version tag (e.g., v1.0.0)
   - ✅ Release notes formatted properly
   - ✅ Both ZIP files attached
   - ✅ Download links work
   - ✅ Marked as "Latest" (green badge)

3. **Test the downloads:**
   - Download each ZIP file
   - Extract and verify executables run correctly
   - Test on a clean machine if possible

---

## 📌 Version Numbering

Follow [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

- **MAJOR** (v2.0.0) - Breaking changes, incompatible API changes
- **MINOR** (v1.1.0) - New features, backwards-compatible
- **PATCH** (v1.0.1) - Bug fixes, backwards-compatible

### Examples:
- `v1.0.0` - Initial release
- `v1.0.1` - Bug fix release
- `v1.1.0` - Added new feature
- `v2.0.0` - Complete rewrite or major breaking changes

---

## 🏷️ File Naming Convention

```
vokey_gui_v{VERSION}.zip
vokey_background_v{VERSION}.zip
```

**Examples:**
- `vokey_gui_v1.0.0.zip`
- `vokey_gui_v1.2.3.zip`
- `vokey_background_v2.0.0.zip`

---

## 🔄 Updating an Existing Release

### To edit release notes or title:
1. Go to the release page
2. Click **"Edit release"**
3. Make your changes
4. Click **"Update release"**

### To add more files:
1. Edit the release
2. Upload additional files
3. Update release

### To delete a release:
1. Edit the release
2. Scroll to bottom
3. Click **"Delete this release"**
4. Note: This doesn't delete the Git tag

---

## 🎯 Quick Reference Commands

### Complete Release Workflow

```bash
# 1. Build
cd "vokey"
python scripts\build.py

# 2. Create ZIPs
cd dist
Compress-Archive -Path vokey_gui -DestinationPath vokey_gui_v1.0.0.zip -Force
Compress-Archive -Path vokey_background -DestinationPath vokey_background_v1.0.0.zip -Force

# 3. Commit and push
cd ..
git add .
git commit -m "Release v1.0.0"
git push origin main

# 4. Create and push tag (optional - can be done on GitHub)
git tag v1.0.0
git push origin v1.0.0

# 5. Create release on GitHub (use web interface or gh CLI)
```

---

## 🚨 Troubleshooting

### Issue: Build fails with permission errors
**Solution:**
```bash
scripts\kill_processes.bat
timeout /t 3
python scripts\build.py
```

### Issue: ZIP files too large
**Solution:**
- Ensure you're zipping the folders, not individual files
- Check if unnecessary files are included
- Consider using 7-Zip with better compression

### Issue: Tag already exists
**Solution:**
```bash
# Delete local tag
git tag -d v1.0.0

# Delete remote tag
git push origin :refs/tags/v1.0.0

# Create new tag
git tag v1.0.0
git push origin v1.0.0
```

### Issue: Release doesn't show as "Latest"
**Solution:**
- Edit the release
- Check "Set as the latest release"
- Update release

---

## 📝 Release Checklist Template

Use this checklist for each release:

```markdown
## Release v1.0.0 Checklist

### Pre-Release
- [ ] All features tested
- [ ] Documentation updated
- [ ] Version numbers updated
- [ ] Changelog prepared
- [ ] Known issues documented

### Build
- [ ] Kill all Vokey processes
- [ ] Clean build completed
- [ ] Both executables tested
- [ ] ZIP files created

### Git
- [ ] All changes committed
- [ ] Code pushed to main
- [ ] Tag created (if manual)

### GitHub Release
- [ ] Release created on GitHub
- [ ] Version tag set correctly
- [ ] Title and notes added
- [ ] ZIP files uploaded
- [ ] Marked as latest
- [ ] Downloads verified

### Post-Release
- [ ] Announcement made (if needed)
- [ ] Documentation links updated
- [ ] Issues/discussions monitored
```

---

## 📚 Additional Resources

- [GitHub Releases Documentation](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [Semantic Versioning](https://semver.org/)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [Writing Good Release Notes](https://keepachangelog.com/)

---

**Made with ❤️ using Google Antigravity IDE**
