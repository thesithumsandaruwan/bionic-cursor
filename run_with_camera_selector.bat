@echo off
REM Hand Gesture Mouse Control - Enhanced Launcher
REM This script will first help you select a camera, then start the main application

echo ============================================================
echo HAND GESTURE MOUSE CONTROL - ENHANCED LAUNCHER
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or later from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade requirements
echo Checking dependencies...
pip install -r requirements.txt --quiet

REM Run the enhanced launcher
echo.
echo Starting Hand Gesture Mouse Control Launcher...
echo.
python launcher.py

REM Deactivate virtual environment
deactivate

echo.
echo Launcher finished.
pause
