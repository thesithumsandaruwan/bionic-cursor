import cv2
import time
import config
import os
import sys
import argparse
import threading

from hand_tracker import HandTracker
from gesture_recognizer import GestureRecognizer, GESTURE_IDLE, GESTURE_MOVE, GESTURE_DRAG # Import states
from mouse_controller import MouseController
from ui_manager import UIManager, CameraManager

# Import system tray support (optional)
try:
    from system_tray import create_system_tray
    SYSTEM_TRAY_AVAILABLE = True
except ImportError:
    SYSTEM_TRAY_AVAILABLE = False
    print("System tray functionality not available (missing pystray/PIL)")

def load_selected_camera():
    """Load previously selected camera from file"""
    try:
        if os.path.exists('selected_camera.txt'):
            with open('selected_camera.txt', 'r') as f:
                camera_index = int(f.read().strip())
                print(f"Found saved camera selection: Camera {camera_index}")
                return camera_index
    except Exception as e:
        print(f"Could not load saved camera selection: {e}")
    return None

def main(headless=False, silent=False):
    if not silent:
        print("Starting Hand Gesture Mouse Control...")
        if headless:
            print("Running in headless mode (no camera window)")
        print("Initializing components...")
    
    # Initialize managers
    camera_manager = CameraManager()
    if not headless:
        ui_manager = UIManager()
    
    # Check for previously selected camera
    selected_camera = load_selected_camera()
    
    # Initialize camera with selected camera or default
    if selected_camera is not None:
        if not camera_manager.initialize_camera(selected_camera):
            print(f"Could not open selected camera {selected_camera}, trying default...")
            if not camera_manager.initialize_camera():
                print("Error: Could not open any camera.")
                print(f"Available cameras: {camera_manager.available_cameras}")
                return
    else:
        if not camera_manager.initialize_camera():
            print("Error: Could not open any camera.")
            print(f"Available cameras: {camera_manager.available_cameras}")
            print("Try running launcher.py to select a camera first.")
            return

    camera_info = camera_manager.get_camera_info()
    print(f"Using camera {camera_info['index']} ({camera_info['width']}x{camera_info['height']})")
    print(f"Available cameras: {camera_info['available']}")

    # Initialize our modules  
    hand_tracker = HandTracker()
    mouse_controller = MouseController() # Gets screen dimensions on init
    gesture_recognizer = GestureRecognizer(mouse_controller, hand_tracker)
    
    if not silent:
        print(f"Screen: {mouse_controller.screen_width}x{mouse_controller.screen_height}")
        if not headless:
            print("\nControls:")
            print("  'q' - Quit")
            print("  'c' - Change camera")
            print("  'i' - Toggle instructions")  
            print("  'h' - Show help")
        else:
            print("\nHeadless mode controls:")
            print("  Press Ctrl+C to quit")
        print("\nStarting gesture recognition...")

    # For FPS calculation
    prev_time = 0
    frame_count = 0

    try:
        while True:
            success, frame = camera_manager.read_frame()
            if not success:
                if not silent:
                    print("Failed to read frame, trying to reinitialize camera...")
                if not camera_manager.initialize_camera():
                    if not silent:
                        print("Failed to reinitialize camera. Exiting.")
                    break
                continue

            frame_count += 1

            # Process hand tracking
            if headless:
                # In headless mode, don't draw landmarks to save processing
                processed_image, hand_landmarks_list = hand_tracker.find_hands(frame, draw=False)
            else:
                processed_image, hand_landmarks_list = hand_tracker.find_hands(frame, draw=True)

            current_gesture = GESTURE_IDLE # Default if no hand
            fingers = [False] * 5  # Default finger state

            if hand_landmarks_list: # If any hands are detected
                # Assuming only one hand for now (as per HandTracker default)
                for hand_lm in hand_landmarks_list: 
                    lm_list = hand_tracker.get_landmark_list(hand_lm, camera_info['width'], camera_info['height'])
                    if lm_list:
                        fingers = hand_tracker.fingers_up(lm_list)
                        current_gesture = gesture_recognizer.recognize(lm_list, camera_info['width'], camera_info['height'])
                        # Mouse control actions are now handled within gesture_recognizer.recognize()
            else:
                # If no hand is detected, ensure gesture recognizer knows
                gesture_recognizer.recognize([], camera_info['width'], camera_info['height'])

            if not headless:
                # Calculate FPS
                curr_time = time.time()
                fps = 1 / (curr_time - prev_time) if prev_time > 0 else 0
                prev_time = curr_time
                
                # Draw UI elements
                processed_image = ui_manager.draw_status_info(processed_image, fps, current_gesture, camera_info['index'], gesture_recognizer)
                if hand_landmarks_list:
                    for hand_lm in hand_landmarks_list:
                        lm_list = hand_tracker.get_landmark_list(hand_lm, camera_info['width'], camera_info['height'])
                        if lm_list:
                            processed_image = ui_manager.draw_hand_info(processed_image, lm_list, fingers)
                            break  # Only draw for first hand
                processed_image = ui_manager.draw_instructions(processed_image)

                cv2.imshow('Hand Gesture Mouse Control', processed_image)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    if not silent:
                        print("Quit requested")
                    break
                elif key == ord('c'):
                    if not silent:
                        print("Switching camera...")
                    if camera_manager.switch_camera():
                        camera_info = camera_manager.get_camera_info()
                        if not silent:
                            print(f"Switched to camera {camera_info['index']}")
                    else:
                        if not silent:
                            print("Failed to switch camera")
                elif key == ord('i'):
                    ui_manager.toggle_instructions()
                    if not silent:
                        print("Toggled instructions")
                elif key == ord('h'):
                    ui_manager.show_help()
                    if not silent:
                        print("Showing help")
            else:
                # In headless mode, just check for Ctrl+C
                time.sleep(0.01)  # Small delay to prevent excessive CPU usage
                
                # Print status every 1000 frames in headless mode
                if not silent and frame_count % 1000 == 0:
                    print(f"Processed {frame_count} frames, current gesture: {current_gesture}")

    except KeyboardInterrupt:
        if not silent:
            print("\nInterrupted by user")

    if not silent:
        print("Releasing resources...")
    hand_tracker.close()
    camera_manager.release()
    if not headless:
        cv2.destroyAllWindows()
    if not silent:
        print("Application finished.")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Hand Gesture Mouse Control')
    parser.add_argument('--headless', action='store_true', 
                        help='Run without showing camera window')
    parser.add_argument('--silent', action='store_true', 
                        help='Run with minimal console output')
    parser.add_argument('--tray', action='store_true',
                        help='Run with system tray icon (implies headless)')
    return parser.parse_args()

# Global variables for system tray functionality
app_running = False
main_thread = None

def run_main_app(headless=False, silent=False):
    """Wrapper for main function that can be called from system tray"""
    global app_running
    if not app_running:
        app_running = True
        try:
            main(headless=headless, silent=silent)
        finally:
            app_running = False

def quit_app():
    """Quit callback for system tray"""
    global app_running
    app_running = False
    os._exit(0)

if __name__ == '__main__':
    args = parse_arguments()
    
    # If tray mode is requested
    if args.tray and SYSTEM_TRAY_AVAILABLE:
        print("Starting with system tray...")
        
        # Start main application in background thread
        main_thread = threading.Thread(
            target=lambda: run_main_app(headless=True, silent=args.silent), 
            daemon=True
        )
        main_thread.start()
        
        # Create and run system tray
        tray = create_system_tray(run_main_app, quit_app)
        tray.run()
        
    elif args.tray and not SYSTEM_TRAY_AVAILABLE:
        print("System tray not available. Starting in headless mode instead...")
        main(headless=True, silent=args.silent)
    else:
        # Normal startup
        main(headless=args.headless, silent=args.silent)
