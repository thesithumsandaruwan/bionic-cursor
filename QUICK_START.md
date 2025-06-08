# Hand Gesture Control - Quick Start Guide

## Getting Started in 3 Steps

### 1. Install & Run
- **Double-click** `HandGestureControl_Setup.exe` to install
- **Or** run `HandGestureControl.exe` directly (portable mode)
- **Allow** camera access when prompted

### 2. Position Your Hand
- **Distance**: 1-2 feet from camera
- **Lighting**: Ensure good lighting on your hand
- **Background**: Clean, non-cluttered background works best
- **Hand**: Use your dominant hand for best results

### 3. Start Using Gestures!

## Gesture Commands

| Gesture | Action | How To |
|---------|--------|--------|
| 🖐️ **Open Palm** | Idle/Ready | All fingers extended, palm facing camera |
| 👆 **Move Hand** | Move Cursor | Move your whole hand to control cursor |
| 🤏 **Pinch (Quick)** | Left Click | Touch thumb + index finger briefly |
| 🤏➡️ **Pinch + Move** | Drag & Drop | Hold thumb + index together while moving |
| ✌️ **Two Fingers** | Right Click | Touch index + middle finger together |
| 🤙 **Pinky Up** | Scroll | Only pinky finger up, move up/down |

## Running Modes

### 🖥️ Normal Mode (Default)
```
HandGestureControl.exe
```
- Shows camera window
- See gesture recognition in real-time
- Press 'q' to quit, 'c' to change camera

### 👻 Headless Mode (Background)
```
HandGestureControl.exe --headless
```
- No camera window
- Runs in background
- Use Ctrl+C to quit

### 🔕 Silent Mode (Minimal Output)
```
HandGestureControl.exe --headless --silent
```
- No window, minimal console output
- Best for always-on operation

### 📊 System Tray Mode (Recommended)
```
HandGestureControl.exe --tray
```
- Runs in system tray
- Right-click tray icon for menu
- Easy start/stop controls

## Quick Tips

### ✅ DO
- **Practice** gestures slowly at first
- **Keep** hand steady when making gestures
- **Use** good lighting
- **Position** camera at eye level if possible
- **Start** with system tray mode for daily use

### ❌ DON'T
- **Don't** make gestures too quickly
- **Don't** use multiple hands simultaneously
- **Don't** block the camera view
- **Don't** use in very dark environments

## Troubleshooting Quick Fixes

### 📷 Camera Issues
- **Press 'c'** in normal mode to cycle cameras
- **Close** other apps using the camera (Skype, Teams, etc.)
- **Try** different USB ports
- **Restart** the application

### 🖱️ Mouse Not Moving
- **Check** if hand is visible in camera
- **Ensure** good lighting
- **Keep** hand 1-2 feet from camera
- **Try** making gestures more deliberately

### 🎯 Gestures Not Working
- **Practice** each gesture individually
- **Hold** pinch gestures for 0.5 seconds
- **Make** gestures more pronounced
- **Ensure** fingers are clearly separated

### 💻 Performance Issues
- **Use** `--headless` mode to reduce CPU usage
- **Close** unnecessary applications
- **Ensure** adequate lighting for better recognition

## Keyboard Shortcuts (Normal Mode)

| Key | Action |
|-----|--------|
| `q` | Quit application |
| `c` | Change/cycle camera |
| `i` | Toggle instruction display |
| `h` | Show help information |

## System Tray Menu (Tray Mode)

- **Hand Gesture Control** - Show about dialog
- **Open Camera Window** - Switch to normal mode
- **Restart Headless** - Restart in background
- **Help** - Show gesture help
- **Quit** - Exit application

## Advanced Usage

### Auto-Start with Windows
1. **Right-click** system tray icon
2. **Or** add to Windows startup folder:
   - Press `Win + R`, type `shell:startup`
   - Copy `start_tray.bat` to this folder

### Multiple Cameras
- **Press 'c'** to cycle through available cameras
- **Selection** is automatically saved
- **Restart** application to use saved camera

### Configuration
- **Camera selection** saved in `selected_camera.txt`
- **Gesture thresholds** can be adjusted in `config.py`
- **Sensitivity** settings available for advanced users

## Getting Help

1. **Read** this guide thoroughly
2. **Practice** each gesture individually
3. **Check** the full README.md for detailed information
4. **Try** different lighting conditions
5. **Ensure** camera is working with other applications first

## Performance Expectations

- **CPU Usage**: 10-30% depending on mode and hardware
- **Memory**: ~100-200MB RAM usage
- **Response Time**: ~50-100ms gesture recognition
- **Accuracy**: 85-95% with good lighting and practice

---

**🎉 You're ready to control your computer with hand gestures!**

*Start with system tray mode for the best experience, practice the gestures, and enjoy hands-free computer control!*
