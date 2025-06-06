@echo off
echo.
echo Hand Gesture Mouse Control - Installation Verification
echo =====================================================
echo.

REM Check Python installation
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
) else (
    python --version
    echo ✅ Python is available
)

echo.
echo [2/4] Installing required packages...
pip install opencv-python mediapipe pynput --quiet --upgrade
if errorlevel 1 (
    echo ❌ Failed to install some packages
    echo Please check your internet connection and try again
    pause
    exit /b 1
) else (
    echo ✅ Packages installed successfully
)

echo.
echo [3/4] Testing component imports...
python test_components.py
if errorlevel 1 (
    echo ❌ Component test failed
    pause
    exit /b 1
)

echo.
echo [4/4] Ready to launch!
echo ✅ All checks passed successfully
echo.
echo The application is ready to run.
echo Press any key to start the Hand Gesture Mouse Control...
pause >nul

echo.
echo Starting application...
python main.py
