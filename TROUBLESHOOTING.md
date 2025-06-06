# Troubleshooting Guide

## Common Issues and Solutions

### 1. Camera Not Working

**Problem**: "Error: Could not open any camera" or black screen
**Solutions**:
- Ensure your camera is not being used by another application (Zoom, Skype, etc.)
- Try pressing 'c' to switch cameras if multiple cameras are available
- Check if camera permissions are granted to the application
- Restart the application

### 2. Hand Detection Not Working

**Problem**: Hand is not being detected or gestures are not recognized
**Solutions**:
- Ensure good lighting conditions
- Keep your hand clearly visible to the camera
- Avoid busy backgrounds
- Make sure your hand is within the camera frame
- Try adjusting the `MIN_DETECTION_CONFIDENCE` in `config.py` (lower values = more sensitive)

### 3. Mouse Control Too Sensitive/Not Sensitive Enough

**Problem**: Mouse jumps around or doesn't move enough
**Solutions**:
- Adjust `PINCH_THRESHOLD_CLICK` in `config.py` for click sensitivity
- Modify `SCROLL_SENSITIVITY` for scroll responsiveness
- Enable mouse smoothing in `mouse_controller.py` (uncomment smoothing code)

### 4. Gestures Not Recognized Properly

**Problem**: Wrong gestures are detected or gestures don't work
**Solutions**:
- Practice the gestures as shown in the instructions
- Adjust timing settings in `config.py`:
  - `CLICK_DEBOUNCE_TIME`: Time between clicks
  - `SCROLL_DEBOUNCE_TIME`: Time between scroll actions
- Make sure fingers are clearly extended or folded as required

### 5. Performance Issues

**Problem**: Low FPS or laggy response
**Solutions**:
- Close other applications using the camera
- Reduce camera resolution in `config.py`
- Lower `MIN_DETECTION_CONFIDENCE` and `MIN_TRACKING_CONFIDENCE`
- Ensure good lighting to help MediaPipe process faster

### 6. Installation Issues

**Problem**: Dependencies won't install or import errors
**Solutions**:
- Make sure you have Python 3.8 or higher
- Use a virtual environment:
  ```
  python -m venv hand_gesture_env
  hand_gesture_env\Scripts\activate
  pip install -r requirements.txt
  ```
- On some systems, use `python3` instead of `python`
- If MediaPipe fails to install, try: `pip install --upgrade pip` first

### 7. Permission Issues (Windows)

**Problem**: Mouse control doesn't work or requires admin rights
**Solutions**:
- Run the application as Administrator
- Check Windows security settings for input automation
- Ensure pynput has proper permissions

## Configuration Tips

### For Better Gesture Recognition:
1. Sit 2-3 feet from the camera
2. Use good, even lighting
3. Wear contrasting clothing (avoid hand-colored clothing)
4. Keep a clean background behind your hand

### For Optimal Performance:
1. Close unnecessary applications
2. Use a dedicated webcam if available
3. Ensure stable camera mounting
4. Keep the camera at eye level

## Getting Help

If you continue to have issues:
1. Check the console output for error messages
2. Try adjusting settings in `config.py`
3. Test with different lighting conditions
4. Restart the application
5. Check that all dependencies are properly installed

## Reporting Issues

When reporting issues, please include:
- Your operating system and version
- Python version (`python --version`)
- Error messages from the console
- Camera model and specifications
- Description of what gesture you were trying to perform
