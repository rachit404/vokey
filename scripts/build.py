"""
Python build script for Voice Assistant .exe files
This script builds both GUI and background versions of the application
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def main():
    print("=" * 60)
    print("Voice Assistant Build Script (Python)")
    print("=" * 60)
    print()
    
    # Get the project root directory (parent of scripts/)
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    os.chdir(project_dir)
    
    # Install PyInstaller if needed
    print("Checking PyInstaller installation...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pyinstaller>=6.0.0", "--quiet"],
            check=True
        )
        print("PyInstaller is ready.")
    except subprocess.CalledProcessError:
        print("ERROR: Failed to install PyInstaller")
        return 1
    print()
    
    # Clean previous builds
    print("Cleaning previous builds...")
    for dir_name in ["build", "dist"]:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"  Removed {dir_name}/")
            except PermissionError as e:
                print(f"  Warning: Could not remove {dir_name}/ (some files may be in use)")
                print(f"  Continuing anyway... PyInstaller will overwrite files.")
    print()
    
    # Build GUI version
    print("=" * 60)
    print("Building GUI version (vokey_gui.exe)...")
    print("=" * 60)
    try:
        subprocess.run(
            [sys.executable, "-m", "PyInstaller", "scripts/vokey_gui.spec", "--clean"],
            check=True
        )
        print("GUI build completed successfully!")
    except subprocess.CalledProcessError:
        print("ERROR: GUI build failed!")
        return 1
    print()
    
    # Build background version
    print("=" * 60)
    print("Building background version (vokey_background.exe)...")
    print("=" * 60)
    try:
        subprocess.run(
            [sys.executable, "-m", "PyInstaller", "scripts/vokey_background.spec", "--clean"],
            check=True
        )
        print("Background build completed successfully!")
    except subprocess.CalledProcessError:
        print("ERROR: Background build failed!")
        return 1
    print()
    
    # Summary
    print("=" * 60)
    print("Build completed successfully!")
    print("=" * 60)
    print()
    print("Output locations:")
    print(f"  - GUI version:        dist/vokey_gui/vokey_gui.exe")
    print(f"  - Background version: dist/vokey_background/vokey_background.exe")
    print()
    print("You can now run the executables directly.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
