"""
Comprehensive test for gesture recognition functionality
Run this to test all implemented gestures
"""

import cv2
import time
from hand_tracker import HandTracker
from gesture_recognizer import GestureRecognizer, GESTURE_IDLE, GESTURE_MOVE
from mouse_controller import MouseController
from ui_manager import UIManager, CameraManager

def print_gesture_instructions():
    """Print instructions for testing all gestures"""
    print("\n" + "="*60)
    print("GESTURE TESTING MODE")
    print("="*60)
    print("\nTest each gesture in this order:")
    print("1. IDLE: Show open palm (all fingers extended)")
    print("2. MOVE: Show any hand position (uses whole hand center)")
    print("3. LEFT CLICK: Quick thumb + index finger pinch")
    print("4. DRAG: Hold thumb + index finger pinch and move hand")
    print("5. RIGHT CLICK: Touch index and middle fingertips together")
    print("6. SCROLL: Only pinky up, move up/down")
    print("\nPress 'q' to quit, 'r' to reset gesture state")
    print("Press 'h' to show these instructions again")
    print("="*60)

def display_detailed_info(image, gesture_recognizer, hand_tracker, lm_list, fingers):
    """Display detailed gesture information on the image"""
    h, w = image.shape[:2]
    
    # Get gesture info
    gesture_info = gesture_recognizer.get_gesture_info()
    
    # Display current gesture state
    cv2.putText(image, f"Gesture: {gesture_info['current_gesture']}", 
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Display finger states
    finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
    for i, (name, is_up) in enumerate(zip(finger_names, fingers)):
        color = (0, 255, 0) if is_up else (0, 0, 255)
        cv2.putText(image, f"{name}: {'UP' if is_up else 'DOWN'}", 
                    (10, 70 + i*25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    # Display preparation states
    y_offset = 200
    if gesture_info['left_click_prepared']:
        cv2.putText(image, "LEFT CLICK PREPARED", (10, y_offset), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        y_offset += 30
    
    if gesture_info['right_click_prepared']:
        cv2.putText(image, "RIGHT CLICK PREPARED", (10, y_offset), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        y_offset += 30
    
    if gesture_info['in_scroll_mode']:
        cv2.putText(image, "SCROLL MODE ACTIVE", (10, y_offset), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        y_offset += 30
    
    if gesture_info['is_dragging']:
        cv2.putText(image, "DRAGGING ACTIVE", (10, y_offset), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
        y_offset += 30
    
    # Display distances for debugging
    if lm_list:
        import mediapipe as mp
        mp_hands = mp.solutions.hands
        
        dist_thumb_index = hand_tracker.calculate_distance(
            lm_list, mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP)
        dist_index_middle = hand_tracker.calculate_distance(
            lm_list, mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP)
        
        cv2.putText(image, f"Thumb-Index: {dist_thumb_index:.3f}", 
                    (w-200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(image, f"Index-Middle: {dist_index_middle:.3f}", 
                    (w-200, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return image

def main():
    """Main testing function"""
    print_gesture_instructions()
    
    # Initialize components
    print("Initializing components...")
    camera_manager = CameraManager()
    ui_manager = UIManager()
    
    if not camera_manager.initialize_camera():
        print("Error: Could not open camera.")
        return
    
    camera_info = camera_manager.get_camera_info()
    print(f"Using camera {camera_info['index']} ({camera_info['width']}x{camera_info['height']})")
    
    hand_tracker = HandTracker()
    mouse_controller = MouseController()
    gesture_recognizer = GestureRecognizer(mouse_controller, hand_tracker)
    
    print("Starting gesture testing...")
    print("Show your hand to the camera and try different gestures!")
    
    # Statistics
    gesture_counts = {}
    start_time = time.time()
    frame_count = 0
    
    while True:
        success, frame = camera_manager.read_frame()
        if not success:
            print("Failed to read frame")
            break
        
        frame_count += 1
        
        # Process hand tracking
        processed_image, hand_landmarks_list = hand_tracker.find_hands(frame, draw=True)
        
        current_gesture = GESTURE_IDLE
        fingers = [False] * 5
        lm_list = []
        
        if hand_landmarks_list:
            for hand_lm in hand_landmarks_list:
                lm_list = hand_tracker.get_landmark_list(hand_lm, camera_info['width'], camera_info['height'])
                if lm_list:
                    fingers = hand_tracker.fingers_up(lm_list)
                    current_gesture = gesture_recognizer.recognize(lm_list, camera_info['width'], camera_info['height'])
                    break
        else:
            gesture_recognizer.recognize([], camera_info['width'], camera_info['height'])
        
        # Update statistics
        if current_gesture in gesture_counts:
            gesture_counts[current_gesture] += 1
        else:
            gesture_counts[current_gesture] = 1
        
        # Display detailed information
        processed_image = display_detailed_info(processed_image, gesture_recognizer, hand_tracker, lm_list, fingers)
        
        # Calculate and display FPS
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time if elapsed_time > 0 else 0
        cv2.putText(processed_image, f"FPS: {fps:.1f}", (10, processed_image.shape[0] - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow('Gesture Testing', processed_image)
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            gesture_recognizer.reset_gesture_state()
            print("Gesture state reset!")
        elif key == ord('h'):
            print_gesture_instructions()
        elif key == ord('c'):
            camera_manager.switch_camera()
            camera_info = camera_manager.get_camera_info()
    
    # Print final statistics
    print("\n" + "="*60)
    print("TESTING COMPLETED")
    print("="*60)
    print(f"Total frames processed: {frame_count}")
    print(f"Average FPS: {fps:.1f}")
    print("\nGesture Statistics:")
    for gesture, count in sorted(gesture_counts.items()):
        percentage = (count / frame_count) * 100
        print(f"  {gesture}: {count} frames ({percentage:.1f}%)")
    
    # Cleanup
    hand_tracker.close()
    camera_manager.release()
    cv2.destroyAllWindows()
    print("Testing finished.")

if __name__ == "__main__":
    main()
