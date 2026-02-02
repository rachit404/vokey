@echo off
REM Build script for Voice Assistant .exe files
REM This script builds both GUI and background versions of the application

echo ========================================
echo Voice Assistant Build Script
echo ========================================
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Install/update PyInstaller if needed
echo Checking PyInstaller installation...
pip install pyinstaller>=6.0.0 --quiet
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo.

REM Build GUI version
echo ========================================
echo Building GUI version (vokey_gui.exe)...
echo ========================================
pyinstaller vokey_gui.spec --clean
if errorlevel 1 (
    echo ERROR: GUI build failed!
    pause
    exit /b 1
)
echo.

REM Build background version
echo ========================================
echo Building background version (vokey_background.exe)...
echo ========================================
pyinstaller vokey_background.spec --clean
if errorlevel 1 (
    echo ERROR: Background build failed!
    pause
    exit /b 1
)
echo.

echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Output locations:
echo   - GUI version:        dist\vokey_gui\vokey_gui.exe
echo   - Background version: dist\vokey_background\vokey_background.exe
echo.
echo You can now run the executables directly.
echo.
pause
