import cv2
import time
import config

from hand_tracker import HandTracker
from gesture_recognizer import GestureRecognizer, GESTURE_IDLE, GESTURE_MOVE # Import states
from mouse_controller import MouseController
from ui_manager import UIManager, CameraManager

def main():
    print("Starting Hand Gesture Mouse Control...")
    print("Initializing components...")
    
    # Initialize managers
    camera_manager = CameraManager()
    ui_manager = UIManager()
    
    # Initialize camera
    if not camera_manager.initialize_camera():
        print("Error: Could not open any camera.")
        print(f"Available cameras: {camera_manager.available_cameras}")
        return

    camera_info = camera_manager.get_camera_info()
    print(f"Using camera {camera_info['index']} ({camera_info['width']}x{camera_info['height']})")
    print(f"Available cameras: {camera_info['available']}")

    # Initialize our modules  
    hand_tracker = HandTracker()
    mouse_controller = MouseController() # Gets screen dimensions on init
    gesture_recognizer = GestureRecognizer(mouse_controller, hand_tracker)

    print(f"Screen: {mouse_controller.screen_width}x{mouse_controller.screen_height}")
    print("\nControls:")
    print("  'q' - Quit")
    print("  'c' - Change camera")
    print("  'i' - Toggle instructions")  
    print("  'h' - Show help")
    print("\nStarting gesture recognition...")

    # For FPS calculation
    prev_time = 0

    while True:
        success, frame = camera_manager.read_frame()
        if not success:
            print("Failed to read frame, trying to reinitialize camera...")
            if not camera_manager.initialize_camera():
                print("Failed to reinitialize camera. Exiting.")
                break
            continue

        # Process hand tracking
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
            print("Quit requested")
            break
        elif key == ord('c'):
            print("Switching camera...")
            if camera_manager.switch_camera():
                camera_info = camera_manager.get_camera_info()
                print(f"Switched to camera {camera_info['index']}")
            else:
                print("Failed to switch camera")
        elif key == ord('i'):
            ui_manager.toggle_instructions()
            print("Toggled instructions")
        elif key == ord('h'):
            ui_manager.show_help()
            print("Showing help")

    print("Releasing resources...")
    hand_tracker.close()
    camera_manager.release()
    cv2.destroyAllWindows()
    print("Application finished.")

if __name__ == '__main__':
    main()
