@echo off
REM Hand Gesture Mouse Control - GUI Launcher
REM This script uses the GUI camera selector for better user experience

echo ============================================================
echo HAND GESTURE MOUSE CONTROL - GUI LAUNCHER
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

REM Run the GUI camera selector first
echo.
echo Starting GUI Camera Selector...
echo Close the camera selector window after selecting your camera.
echo.
python camera_selector_gui.py

REM Check if camera was selected
if not exist "selected_camera.txt" (
    echo No camera selected. Exiting.
    pause
    goto :cleanup
)

REM Run the main application
echo.
echo Starting Hand Gesture Mouse Control...
echo.
python main.py

:cleanup
REM Deactivate virtual environment
deactivate

echo.
echo Application finished.
pause
