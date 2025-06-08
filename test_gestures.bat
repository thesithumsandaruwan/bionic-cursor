@echo off
REM Enhanced Gesture Testing - Test all gesture functionalities
REM This script runs the comprehensive gesture testing tool

echo ============================================================
echo HAND GESTURE MOUSE CONTROL - GESTURE TESTING
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

echo.
echo Starting Gesture Testing Tool...
echo This will help you test all gesture functionalities:
echo - Idle (open palm)
echo - Move (index finger pointing)
echo - Left click (thumb-index pinch)
echo - Right click (thumb-middle pinch)
echo - Scroll (pinky up, move up/down)
echo.
echo Press 'q' to quit, 'r' to reset, 'h' for help
echo.

REM Run the gesture testing tool
python test_gestures.py

REM Deactivate virtual environment
deactivate

echo.
echo Gesture testing finished.
pause
