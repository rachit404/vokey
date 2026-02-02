@echo off
REM Kill all Vokey-related processes before building
echo =====================================================
echo Killing Vokey Processes
echo =====================================================
echo.

echo Checking for running Vokey processes...

REM Kill vokey_gui.exe
tasklist /FI "IMAGENAME eq vokey_gui.exe" 2>NUL | find /I /N "vokey_gui.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo   Found vokey_gui.exe - Terminating...
    taskkill /F /IM vokey_gui.exe >NUL 2>&1
    timeout /t 1 /nobreak >NUL
) else (
    echo   vokey_gui.exe not running
)

REM Kill vokey_background.exe
tasklist /FI "IMAGENAME eq vokey_background.exe" 2>NUL | find /I /N "vokey_background.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo   Found vokey_background.exe - Terminating...
    taskkill /F /IM vokey_background.exe >NUL 2>&1
    timeout /t 1 /nobreak >NUL
) else (
    echo   vokey_background.exe not running
)

REM Kill python processes running vokey scripts
echo   Checking for Python processes running vokey...
taskkill /F /FI "WINDOWTITLE eq *vokey*" >NUL 2>&1
timeout /t 1 /nobreak >NUL

echo.
echo All Vokey processes terminated.
echo Waiting for files to unlock...
timeout /t 2 /nobreak >NUL
echo.
