@echo off
echo.
echo ============================================================
echo Voice Assistant - New Dependencies Installation
echo ============================================================
echo.
echo Installing cursor tracking and system tray dependencies...
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Install new dependencies
echo Installing pywin32 (Windows cursor tracking)...
pip install pywin32>=306

echo.
echo Installing pystray (System tray icon)...
pip install pystray>=0.19.5

echo.
echo Installing pillow (Icon generation)...
pip install pillow>=10.0.0

echo.
echo ============================================================
echo Installation complete!
echo ============================================================
echo.
echo You can now run the voice assistant in background mode:
echo   - Double-click: start_background.pyw
echo   - Or run: pythonw start_background.pyw
echo.
pause
