@echo off
echo Starting Hand Gesture Control in headless mode (no camera window)...
cd /d "%~dp0"
HandGestureControl.exe --headless
