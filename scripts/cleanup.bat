@echo off
REM Cleanup script for vokey repository
echo Cleaning repository...
echo.

if exist venv (
    echo Deleting venv/...
    rmdir /s /q venv
)

if exist __pycache__ (
    echo Deleting __pycache__/...
    rmdir /s /q __pycache__
)

if exist build (
    echo Deleting build/...
    rmdir /s /q build
)

if exist dist (
    echo Deleting dist/...
    rmdir /s /q dist
)

if exist history.db (
    echo Deleting history.db...
    del /f /q history.db
)

if exist vokey_20260202.log (
    echo Deleting vokey_20260202.log...
    del /f /q vokey_20260202.log
)

if exist 0.19.5 (
    echo Deleting 0.19.5...
    del /f /q 0.19.5
)

if exist 10.0.0 (
    echo Deleting 10.0.0...
    del /f /q 10.0.0
)

if exist 306 (
    echo Deleting 306...
    del /f /q 306
)

echo.
echo Cleanup completed successfully!
echo.
dir /b
pause
