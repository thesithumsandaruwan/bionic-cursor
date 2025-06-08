@echo off
echo Testing Hand Gesture Mouse Control Fixes
echo ========================================
echo.
echo Testing the following fixes:
echo 1. Cursor movement - should now move naturally (right hand = right cursor)
echo 2. Right-click gesture - changed to thumb + ring finger pinch
echo.
echo Press any key to start the test application...
pause > nul
echo.
echo Starting test application...
python test_gestures.py
echo.
echo Test completed. Press any key to exit...
pause > nul
