# Hand Gesture Mouse Control

![Hand Gesture Control](https://img.shields.io/badge/Computer%20Vision-Hand%20Gesture%20Control-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-brightgreen)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5%2B-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.8%2B-orange)

A computer vision application that lets you control your mouse cursor and perform common mouse actions using hand gestures. Say goodbye to your physical mouse and navigate your computer with natural hand movements!

## 📝 Overview

This application uses your webcam to track your hand movements and translates them into mouse actions:

- **Move cursor**: Point with your index finger
- **Left click**: Pinch your thumb and index finger
- **Right click**: Pinch your thumb and middle finger
- **Scroll**: Raise your pinky finger and move it up or down
- **Idle**: Open palm (all fingers extended)

The system is designed to be intuitive and responsive, offering a new way to interact with your computer without traditional input devices.

## ✨ Features

- **Real-time hand tracking**: Uses MediaPipe's hand landmark detection for accurate finger tracking
- **Natural gesture recognition**: Intuitive gestures for common mouse actions
- **Visual feedback**: On-screen display shows FPS and current gesture
- **Configurable sensitivity**: Easily adjust thresholds to match your preferences

## 🛠️ Technologies Used

- **Python**: Core programming language
- **OpenCV**: For webcam access and image processing
- **MediaPipe**: For advanced hand tracking and landmark detection
- **pynput**: For controlling the mouse cursor
- **tkinter**: For obtaining screen dimensions

## 🔧 Installation

1. **Clone the repository**
   ```
   git clone https://github.com/yourusername/hand-gesture-mouse-control.git
   cd hand-gesture-mouse-control
   ```

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```
   
   This will install the following packages:
   - opencv-python
   - mediapipe
   - pynput

3. **Run the application**
   ```
   python main.py
   ```

## 🎮 Usage Instructions

1. **Launch the application** by running `main.py`
2. **Position your hand** in front of your webcam
3. **Use the following gestures**:
   - **Move cursor**: Extend your thumb and index finger in an "L" shape
   - **Left click**: Bring your thumb and index finger together (pinch)
   - **Right click**: Bring your thumb and middle finger together (pinch)
   - **Scroll**: Raise only your pinky finger and move it up/down
   - **Idle state**: Extend all fingers (open palm)
4. **Quit the application** by pressing 'q' in the webcam window

## 📊 Project Structure

- **main.py**: Entry point of the application
- **hand_tracker.py**: Handles hand detection and landmark extraction
- **gesture_recognizer.py**: Interprets hand landmarks as specific gestures
- **mouse_controller.py**: Translates gestures into mouse actions

## ⚙️ Customization

You can adjust various parameters in the code to customize the behavior:

- In **gesture_recognizer.py**:
  - `pinch_threshold_click`: Distance threshold for click detection
  - `scroll_sensitivity`: Sensitivity of scroll gestures
  - `CLICK_DEBOUNCE_TIME`: Time between registered clicks

## 🚀 Future Improvements

- [ ] Support for dragging and dropping
- [ ] Personalized gesture profiles
- [ ] Machine learning for improved gesture recognition
- [ ] System tray integration
- [ ] Support for multi-monitor setups
- [ ] Startup with Windows option

## 🤝 Contributing

Contributions are welcome! Feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- The [MediaPipe](https://mediapipe.dev/) team for their excellent hand tracking solution
- The [OpenCV](https://opencv.org/) community for computer vision tools
- [pynput](https://pynput.readthedocs.io/) developers for the mouse control library

---

*Made with ❤️ for human-computer interaction*
