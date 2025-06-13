# Hand Gesture Mouse Control

![Hand Gesture Control](https://img.shields.io/badge/Computer%20Vision-Hand%20Gesture%20Control-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-brightgreen)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5%2B-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.8%2B-orange)

A sophisticated computer vision application that lets you control your mouse cursor and perform common mouse actions using natural hand gestures. Experience a new way to interact with your computer without traditional input devices!

## 🎥 Demo

*Show your hand to the camera and start controlling your mouse with intuitive gestures!*

## 📝 Overview

This application uses your webcam to track your hand movements in real-time and translates them into precise mouse actions:

- **🖱️ Move cursor**: Move your whole hand to control the cursor naturally
- **🎯 Drag & Drop**: Pinch thumb and index finger, hold and move to drag items
- **👆 Left click**: Quick pinch of thumb and index finger together
- **🖕 Right click**: Touch index and middle fingertips together
- **📜 Scroll**: Raise your pinky finger and move it up or down
- **✋ Idle**: Open palm (all fingers extended) to pause control

The system features intelligent gesture recognition with configurable sensitivity and visual feedback for an optimal user experience.

## ✨ Key Features

### Core Functionality
- **Real-time hand tracking**: Advanced MediaPipe hand landmark detection
- **Natural gesture recognition**: Intuitive gestures that feel natural
- **Precise mouse control**: Smooth cursor movement with configurable sensitivity
- **Multi-gesture support**: Click, scroll, and navigate seamlessly

### User Interface
- **Interactive instructions**: On-screen help that appears on startup
- **Visual feedback**: Real-time display of FPS, current gesture, and finger states
- **Camera switching**: Easy switching between multiple cameras
- **Customizable display**: Toggle instructions and status information

### Configuration & Control
- **Configurable settings**: Easily adjust sensitivity and timing parameters
- **Camera management**: Automatic detection and switching of available cameras
- **Keyboard shortcuts**: Quick access to common functions
- **Performance monitoring**: Real-time FPS and gesture state display

## 🛠️ Technologies Used

- **Python 3.8+**: Core programming language
- **OpenCV**: Computer vision and webcam access
- **MediaPipe**: Advanced hand tracking and landmark detection
- **pynput**: Cross-platform mouse control
- **tkinter**: System integration for screen dimensions

## 🔧 Quick Start

### Option 1: Enhanced Launch with Camera Selection (Windows)
1. **Download/Clone** the repository
2. **Double-click** `run_with_camera_selector.bat` - it will help you select the best camera and then start the application
3. **Alternative**: Use `run_gui.bat` for a graphical camera selector with live preview

### Option 2: Easy Launch (Windows)
1. **Download/Clone** the repository
2. **Double-click** `run.bat` - it will automatically install dependencies and start the application

### Option 3: Manual Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hand-gesture-mouse-control.git
   cd hand-gesture-mouse-control
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## 📹 Camera Selection

The application now includes advanced camera selection features:

### Automatic Camera Selection
- **GUI Selector**: Run `run_gui.bat` for a user-friendly interface with live camera preview
- **Console Selector**: Run `select_camera.bat` for a text-based camera selection
- **Integrated Launcher**: Use `run_with_camera_selector.bat` for the complete experience

### Camera Selection Features
- **Live Preview**: See exactly what each camera captures before selecting
- **Multiple Camera Support**: Automatically detects all available cameras
- **Resolution Display**: Shows camera resolution and capabilities
- **Persistent Selection**: Remembers your camera choice for future sessions
- **Fallback Options**: Gracefully handles camera connection issues

### Standalone Camera Tools
- **`camera_selector.py`**: Console-based camera selection tool
- **`camera_selector_gui.py`**: GUI-based camera selector with live preview
- **`launcher.py`**: Integrated launcher that combines camera selection with the main app

## 🎮 Usage Guide

### Getting Started
1. **Launch** the application using `run.bat` or `python main.py`
2. **Position** your hand clearly in front of the camera
3. **Follow** the on-screen instructions that appear automatically
4. **Practice** the gestures to get comfortable with the controls

### Gesture Reference
| Gesture | Action | Description |
|---------|--------|-------------|
| 🖐️ **Whole Hand** | Move Cursor | Move your entire hand to control cursor naturally |
| 🎯 **Hold Pinch + Move** | Drag & Drop | Pinch thumb + index, hold and move to drag items |
| 🤏 **Quick Thumb + Index Pinch** | Left Click | Quick pinch of thumb and index fingertips |
| 🤞 **Index + Middle Touch** | Right Click | Touch index and middle fingertips together |
| 🖐️ **Pinky Up** | Scroll Mode | Raise only pinky finger, then move up/down to scroll |
| ✋ **Open Palm** | Idle State | Extend all fingers to pause mouse control |

### Keyboard Controls
- **'q'** - Quit application
- **'c'** - Switch to next available camera
- **'i'** - Toggle instruction display on/off
- **'h'** - Show help instructions again

## ⚙️ Configuration

Customize the application by editing `config.py`:

```python
# Gesture sensitivity
PINCH_THRESHOLD_CLICK = 0.06        # Lower = more sensitive clicks
SCROLL_SENSITIVITY = 0.1            # Higher = faster scrolling

# Timing settings  
CLICK_DEBOUNCE_TIME = 0.3           # Prevent double-clicks
SCROLL_DEBOUNCE_TIME = 0.2          # Scroll responsiveness

# Camera settings
CAMERA_WIDTH = 640                  # Camera resolution
CAMERA_HEIGHT = 480
```

## 📊 Project Structure

```
hand-gesture-mouse-control/
├── main.py                      # Main application entry point
├── hand_tracker.py              # Hand detection and landmark extraction  
├── gesture_recognizer.py        # Gesture interpretation and mouse control
├── mouse_controller.py          # Mouse action implementation
├── ui_manager.py               # User interface and visual feedback
├── config.py                   # Configuration settings
├── camera_selector.py          # Console-based camera selection
├── camera_selector_gui.py      # GUI-based camera selector with preview
├── launcher.py                 # Integrated launcher with camera selection
├── requirements.txt            # Python dependencies
├── run.bat                     # Basic Windows launcher script
├── run_gui.bat                 # GUI launcher with camera selection
├── run_with_camera_selector.bat # Enhanced launcher with camera selection
├── select_camera.bat           # Standalone camera selector
├── setup_and_run.bat          # Installation verification script
├── test_components.py         # Component testing utilities
├── README.md                  # This file
├── TROUBLESHOOTING.md         # Common issues and solutions
└── PROJECT_SUMMARY.md         # Detailed project overview
```

## 🚀 Advanced Features

### Camera Management
- **Auto-detection** of available cameras
- **Hot-swapping** between cameras during runtime
- **Fallback handling** for camera disconnection

### Performance Optimization
- **Real-time FPS monitoring**
- **Configurable detection thresholds**
- **Efficient landmark processing**

### User Experience
- **Progressive instruction hiding** (auto-hide after 10 seconds)
- **Color-coded gesture feedback**
- **Finger state visualization**
- **Smooth gesture transitions**

## 🔧 Troubleshooting

For common issues and solutions, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

**Quick fixes:**
- **Camera issues**: Press 'c' to switch cameras
- **Poor detection**: Improve lighting and background contrast
- **Sensitivity**: Adjust thresholds in `config.py`
- **Performance**: Close other camera applications

## 🎯 Future Enhancements

- [ ] **Drag & Drop**: Hold and drag gesture support
- [ ] **Multi-finger gestures**: Complex gesture combinations
- [ ] **Gesture customization**: User-defined gesture mapping
- [ ] **Machine learning**: Personalized gesture recognition
- [ ] **System integration**: Windows startup and system tray
- [ ] **Multi-monitor**: Full multi-display support
- [ ] **Voice commands**: Hybrid voice + gesture control

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to new functions
- Test with different cameras and lighting conditions
- Update documentation for new features

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- **[MediaPipe Team](https://mediapipe.dev/)** - Exceptional hand tracking technology
- **[OpenCV Community](https://opencv.org/)** - Computer vision foundation
- **[pynput Developers](https://pynput.readthedocs.io/)** - Cross-platform input control
- **Contributors** - Thank you for making this project better!

## 📈 Project Stats

- **Languages**: Python
- **Dependencies**: 3 core libraries
- **Platform**: Cross-platform (Windows, macOS, Linux)
- **License**: MIT (Open Source)

---

*Made with ❤️ for intuitive human-computer interaction*

**⭐ Star this repo if you found it useful!**
