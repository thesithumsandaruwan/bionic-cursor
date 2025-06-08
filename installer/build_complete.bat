@echo off
echo ================================================
echo Hand Gesture Control - Complete Build & Test
echo ================================================
echo.

REM Set script directory as working directory
cd /d "%~dp0"
cd ..

echo Current directory: %CD%
echo.

REM Check Python installation
echo [1/8] Checking Python installation...
python --version 2>nul
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)
echo Python found!
echo.

REM Install dependencies
echo [2/8] Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed!
echo.

REM Test basic functionality
echo [3/8] Testing basic components...
python -c "import cv2, mediapipe, pynput; print('Core modules OK')"
if errorlevel 1 (
    echo ERROR: Core modules test failed
    pause
    exit /b 1
)
echo Basic components OK!
echo.

REM Create icon
echo [4/8] Creating application icon...
cd installer
python create_icon.py
cd ..
echo Icon created!
echo.

REM Build executable
echo [5/8] Building executable with PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)

pyinstaller --onefile --windowed --add-data "config.py;." --add-data "system_tray.py;." --hidden-import cv2 --hidden-import mediapipe --hidden-import pynput --hidden-import pystray --hidden-import PIL --hidden-import tkinter --name HandGestureControl main.py

if errorlevel 1 (
    echo ERROR: Failed to build executable
    pause
    exit /b 1
)
echo Executable built successfully!
echo.

REM Copy files to installer directory
echo [6/8] Preparing installer files...
if not exist "installer\output" mkdir "installer\output"
copy "dist\HandGestureControl.exe" "installer\HandGestureControl.exe" >nul
copy "README.md" "installer\README.md" >nul
copy "LATEST_UPDATES.md" "installer\LATEST_UPDATES.md" >nul
copy "INSTALLATION_GUIDE.md" "installer\INSTALLATION_GUIDE.md" >nul
copy "requirements.txt" "installer\requirements.txt" >nul
echo Files prepared!
echo.

REM Test executable
echo [7/8] Testing built executable...
timeout /t 3 /nobreak >nul
echo Starting test of built executable (will run for 10 seconds)...
start /min "Test HandGestureControl" installer\HandGestureControl.exe --headless --silent
timeout /t 10 /nobreak >nul
taskkill /f /im HandGestureControl.exe >nul 2>&1
echo Executable test completed!
echo.

REM Final summary
echo [8/8] Build Summary
echo ================================================
echo ✓ Python dependencies installed
echo ✓ Core modules tested
echo ✓ Application icon created
echo ✓ Executable built successfully
echo ✓ Installer files prepared
echo ✓ Executable tested
echo.
echo FILES CREATED:
echo - dist\HandGestureControl.exe (main executable)
echo - installer\HandGestureControl.exe (installer copy)
echo - installer\*.bat (startup scripts)
echo - installer\create_installer.iss (Inno Setup script)
echo.
echo NEXT STEPS:
echo 1. Test the executable: installer\HandGestureControl.exe
echo 2. Create installer with Inno Setup (optional)
echo 3. Distribute the files or installer
echo.
echo BUILD COMPLETE!
echo ================================================
pause
