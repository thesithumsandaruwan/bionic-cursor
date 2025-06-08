@echo off
echo ================================================
echo Hand Gesture Control - Installer Builder
echo ================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python first: https://python.org
    pause
    exit /b 1
)

echo Python found. Starting build process...
echo.

REM Install required packages
echo Installing required packages...
pip install pyinstaller opencv-python mediapipe pynput Pillow pystray

echo.
echo Building installer...
python build_installer.py

echo.
echo ================================================
echo Build process complete!
echo ================================================
echo.
echo Next steps:
echo 1. Check the 'installer' folder for the built files
echo 2. If you have Inno Setup installed, compile 'create_installer.iss'
echo 3. Otherwise, you can distribute the files manually
echo.
pause
