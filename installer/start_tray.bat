@echo off
echo Starting Hand Gesture Control with system tray...
cd /d "%~dp0"
HandGestureControl.exe --tray --silent
