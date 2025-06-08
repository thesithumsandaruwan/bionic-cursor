@echo off
REM Camera Selector - Standalone Tool
REM Use this to test camera selection separately

echo ============================================================
echo HAND GESTURE MOUSE CONTROL - CAMERA SELECTOR
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

REM Run the camera selector
echo.
echo Starting Camera Selector...
echo.
python camera_selector.py

REM Deactivate virtual environment
deactivate

echo.
echo Camera selector finished.
pause
