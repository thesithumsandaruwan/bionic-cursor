# Hand Gesture Control - Installation Guide

## Windows Installer

### Quick Installation (Recommended)

1. **Download** the `HandGestureControl_Setup.exe` installer
2. **Run** the installer as Administrator
3. **Follow** the installation wizard
4. **Choose** your preferred startup option:
   - Normal mode (with camera window)
   - System tray mode (runs in background)
   - Manual start only

### Manual Installation

If you prefer to build from source:

#### Prerequisites
- Python 3.8 or higher
- Windows 10/11
- Webcam or external camera

#### Build Steps

1. **Clone or download** the source code
2. **Open Command Prompt** in the project directory
3. **Run the build script**:
   ```cmd
   cd installer
   build.bat
   ```
4. **Wait** for the build process to complete
5. **Find** the built files in the `installer` folder

#### Alternative Build Method

```cmd
# Install dependencies
pip install -r requirements.txt
pip install pyinstaller pystray

# Build executable
pyinstaller --onefile --windowed main.py --name HandGestureControl

# The executable will be in the dist folder
```

## Running the Application

### Different Modes

1. **Normal Mode** (with camera window)
   ```cmd
   HandGestureControl.exe
   ```
   - Shows camera feed
   - Displays gesture recognition status
   - Interactive controls

2. **Headless Mode** (no camera window)
   ```cmd
   HandGestureControl.exe --headless
   ```
   - Runs in background
   - No camera window
   - Console output only

3. **Silent Mode** (minimal output)
   ```cmd
   HandGestureControl.exe --headless --silent
   ```
   - No camera window
   - Minimal console output
   - Best for background operation

4. **System Tray Mode** (with tray icon)
   ```cmd
   HandGestureControl.exe --tray
   ```
   - Runs in background
   - System tray icon with menu
   - Right-click tray icon for options

### Batch Files

The installer creates convenient batch files:

- `start_normal.bat` - Normal mode with camera window
- `start_headless.bat` - Headless mode
- `start_silent.bat` - Silent headless mode
- `start_tray.bat` - System tray mode

## Startup Configuration

### Auto-Start with Windows

During installation, you can choose to start Hand Gesture Control automatically with Windows. This uses system tray mode by default.

To manually add to startup:
1. Open `Run` dialog (Windows + R)
2. Type `shell:startup` and press Enter
3. Copy `start_tray.bat` to this folder

### Camera Selection

On first run, you may need to select your camera:
1. Run the application normally
2. If camera fails, try pressing 'c' to cycle cameras
3. Your selection will be saved automatically

## Troubleshooting

### Common Issues

**Camera not detected:**
- Check camera connections
- Try different USB ports
- Close other applications using the camera
- Press 'c' in the application to cycle cameras

**Gestures not recognized:**
- Ensure good lighting
- Keep hand 1-2 feet from camera
- Practice gestures slowly
- Check camera positioning

**Application won't start:**
- Run as Administrator
- Check Windows Defender/Antivirus
- Verify camera permissions
- Try different startup modes

**High CPU usage:**
- Use headless mode (`--headless`)
- Close unnecessary applications
- Ensure adequate lighting for better recognition

### Performance Tips

1. **Good Lighting**: Ensure your camera area is well-lit
2. **Clean Background**: Avoid cluttered backgrounds behind your hand
3. **Stable Position**: Keep camera steady and at consistent distance
4. **Practice**: Spend time practicing gestures for better recognition
5. **Close Unused Apps**: Close other applications using the camera

### System Requirements

**Minimum:**
- Windows 10 (64-bit)
- Python 3.8+ (for source installation)
- 4GB RAM
- Webcam or USB camera
- 500MB free disk space

**Recommended:**
- Windows 11 (64-bit)
- 8GB RAM
- HD Webcam (720p or higher)
- Dedicated graphics card (for better performance)
- SSD storage

## Uninstallation

### Using Windows Settings
1. Open Windows Settings
2. Go to Apps & Features
3. Find "Hand Gesture Control"
4. Click Uninstall

### Manual Removal
1. Delete the installation folder
2. Remove startup entries if added manually
3. Delete any saved configuration files

## Support

For issues or questions:
1. Check the troubleshooting guide above
2. Review the README.md file
3. Check for updates on the project page
4. Report bugs through the issue tracker

## Updates

The application checks for updates automatically. To manually update:
1. Download the latest installer
2. Run the new installer (it will update existing installation)
3. Restart the application
