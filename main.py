import cv2
import time

from hand_tracker import HandTracker
from gesture_recognizer import GestureRecognizer, GESTURE_IDLE, GESTURE_MOVE # Import states
from mouse_controller import MouseController

def main():
    print("Starting Hand Gesture Mouse Control...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Initialize our modules
    hand_tracker = HandTracker(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    mouse_controller = MouseController() # Gets screen dimensions on init
    gesture_recognizer = GestureRecognizer(mouse_controller, hand_tracker)

    print(f"Webcam opened ({frame_width}x{frame_height}). Screen: {mouse_controller.screen_width}x{mouse_controller.screen_height}. Press 'q' to quit.")

    # For FPS calculation
    prev_time = 0

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Process hand tracking
        # The image is flipped within hand_tracker.find_hands for selfie view and RGB conversion
        processed_image, hand_landmarks_list = hand_tracker.find_hands(frame, draw=True)

        current_gesture = GESTURE_IDLE # Default if no hand

        if hand_landmarks_list: # If any hands are detected
            # Assuming only one hand for now (as per HandTracker default)
            for hand_lm in hand_landmarks_list: 
                lm_list = hand_tracker.get_landmark_list(hand_lm, frame_width, frame_height)
                if lm_list:
                    current_gesture = gesture_recognizer.recognize(lm_list, frame_width, frame_height)
                    # Mouse control actions are now handled within gesture_recognizer.recognize()
        else:
            # If no hand is detected, ensure gesture recognizer knows
            gesture_recognizer.recognize([], frame_width, frame_height) 

        # Calculate and display FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        cv2.putText(processed_image, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(processed_image, f"Gesture: {current_gesture}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow('Hand Gesture Control', processed_image)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    print("Releasing resources...")
    hand_tracker.close()
    cap.release()
    cv2.destroyAllWindows()
    print("Application finished.")

if __name__ == '__main__':
    main()

# Helper function (example) - moved to MouseController or not used
# def map_value(value, in_min, in_max, out_min, out_max):
#     return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
