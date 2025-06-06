import mediapipe as mp
import cv2
import math

class HandTracker:
    def __init__(self, max_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.results = None

    def find_hands(self, image, draw=True):
        """
        Processes an image to find hand landmarks.
        image: BGR image from OpenCV.
        draw: Whether to draw landmarks on the image.
        Returns the image (with or without drawings) and hand landmarks.
        """
        # Flip the image horizontally for a later selfie-view display,
        # and convert the BGR image to RGB.
        img_rgb = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        img_rgb.flags.writeable = False
        self.results = self.hands.process(img_rgb)

        # Prepare image for drawing (convert back to BGR if it was RGB)
        # The input image to this function is BGR, so we use the flipped one for drawing
        output_image = cv2.flip(image, 1) # Use the flipped BGR for drawing

        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    output_image, # Draw on the flipped BGR image
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())
        return output_image, self.results.multi_hand_landmarks

    def get_landmark_list(self, hand_landmarks, frame_width, frame_height):
        """
        Extracts landmark coordinates into a list.
        hand_landmarks: A single hand_landmarks object from MediaPipe results.
        frame_width, frame_height: Dimensions of the camera frame for denormalization (optional).
        Returns a list of [id, x, y, z] for each landmark.
        """
        lm_list = []
        if hand_landmarks:
            for id, lm in enumerate(hand_landmarks.landmark):
                # cx, cy, cz are normalized coordinates (0.0 to 1.0)
                # Denormalize if needed, but for gesture recognition, relative positions are often enough.
                # For mouse movement, we'll use normalized values directly with frame dimensions.
                lm_list.append([id, lm.x, lm.y, lm.z])
        return lm_list

    def fingers_up(self, lm_list):
        """
        Checks which fingers are extended upwards.
        lm_list: List of landmark coordinates [id, x, y, z].
        Returns a list of 5 booleans (thumb, index, middle, ring, pinky).
        Assumes hand is mostly upright.
        """
        if not lm_list or len(lm_list) < 21: # Need all 21 landmarks
            return [False, False, False, False, False]

        fingers = []
        tip_ids = [4, 8, 12, 16, 20] # Landmark IDs for finger tips
        pip_ids = [3, 6, 10, 14, 18] # Landmark IDs for finger PIP joints (second joint from tip)

        # Thumb (different logic due to its structure)
        # Check if thumb tip is to the left (for right hand) or right (for left hand) of PIP
        # This simple y-coordinate check is often sufficient for upright hand
        if lm_list[tip_ids[0]][1] > lm_list[pip_ids[0]][1]: # For a flipped image (selfie view)
            fingers.append(True) # Thumb is to the right of its PIP (appears left for user)
        else:
            fingers.append(False)

        # Other 4 fingers
        for i in range(1, 5):
            if lm_list[tip_ids[i]][2] < lm_list[pip_ids[i]][2]: # Tip Y is above PIP Y
                fingers.append(True)
            else:
                fingers.append(False)
        return fingers

    def calculate_distance(self, lm_list, p1_id, p2_id):
        """
        Calculates the 2D Euclidean distance between two landmarks.
        lm_list: List of landmark coordinates [id, x, y, z].
        p1_id, p2_id: Landmark IDs.
        Returns the distance.
        """
        if not lm_list or max(p1_id, p2_id) >= len(lm_list):
            return float('inf') # Or handle error appropriately
        
        p1 = lm_list[p1_id]
        p2 = lm_list[p2_id]
        # Using normalized x, y for distance calculation. Scale doesn't matter for pinch detection.
        distance = math.sqrt((p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)
        return distance

    def close(self):
        self.hands.close()

if __name__ == '__main__':
    # Example Usage (requires a webcam)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam for HandTracker test.")
        exit()

    tracker = HandTracker()
    print("HandTracker test running. Press 'q' to quit.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        processed_image, hand_landmarks_list = tracker.find_hands(frame)

        if hand_landmarks_list:
            for hand_lm in hand_landmarks_list: # Iterate if multiple hands allowed
                lm_list = tracker.get_landmark_list(hand_lm, frame.shape[1], frame.shape[0])
                if lm_list:
                    # print(f"Landmarks: {lm_list}")
                    fingers = tracker.fingers_up(lm_list)
                    print(f"Fingers Up: {fingers}")
                    
                    # Example: Distance between thumb tip and index finger tip
                    dist_thumb_index = tracker.calculate_distance(lm_list, 4, 8)
                    print(f"Distance Thumb-Index: {dist_thumb_index:.4f}")

        cv2.imshow("Hand Tracker Test", processed_image)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    
    tracker.close()
    cap.release()
    cv2.destroyAllWindows()
    print("HandTracker test finished.")
