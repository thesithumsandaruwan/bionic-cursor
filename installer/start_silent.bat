@echo off
REM Start Hand Gesture Control in silent headless mode (no output, no window)
cd /d "%~dp0"
HandGestureControl.exe --headless --silent
