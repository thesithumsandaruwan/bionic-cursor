import time
import math
import config
from mouse_controller import MouseController # Assuming mouse_controller.py is in the same directory
import mediapipe as mp # For HandLandmark enum

# For gesture state management
GESTURE_NONE = "none"
GESTURE_IDLE = "idle" # Resting hand
GESTURE_MOVE = "move" # Hand moving the cursor
GESTURE_LEFT_CLICK_READY = "left_click_ready" # Poised for left click
GESTURE_LEFT_CLICK_ACTION = "left_click_action"
GESTURE_RIGHT_CLICK_READY = "right_click_ready" # Poised for right click
GESTURE_RIGHT_CLICK_ACTION = "right_click_action"
GESTURE_SCROLL_READY = "scroll_ready"
GESTURE_SCROLL_UP_ACTION = "scroll_up_action"
GESTURE_SCROLL_DOWN_ACTION = "scroll_down_action"

class GestureRecognizer:
    def __init__(self, mouse_controller: MouseController, hand_tracker):
        self.mouse_controller = mouse_controller
        self.hand_tracker = hand_tracker # To use its methods like calculate_distance, fingers_up
        self.mp_hands = mp.solutions.hands # For HandLandmark enum

        self.current_gesture = GESTURE_IDLE
        self.last_gesture_time = time.time()
        self.last_click_time = 0
        self.last_scroll_time = 0
        
        self.prev_hand_center_x = None
        self.prev_hand_center_y = None

        # Load thresholds from config
        self.pinch_threshold_click = config.PINCH_THRESHOLD_CLICK
        self.scroll_pinch_threshold = config.SCROLL_PINCH_THRESHOLD
        self.scroll_sensitivity = config.SCROLL_SENSITIVITY
        self.click_debounce_time = config.CLICK_DEBOUNCE_TIME
        self.scroll_debounce_time = config.SCROLL_DEBOUNCE_TIME
        self.idle_timeout = config.IDLE_TIMEOUT

        # Scroll gesture parameters
        self.scroll_ref_y = None # Y-coordinate of pinky base when scroll gesture starts

    def _calculate_hand_center(self, lm_list):
        if not lm_list or len(lm_list) < 21:
            return None, None
        # Use wrist (0) and MCP of middle finger (9) as a simple center proxy
        x_coords = [lm_list[0][1], lm_list[9][1]]
        y_coords = [lm_list[0][2], lm_list[9][2]]
        center_x = sum(x_coords) / len(x_coords)
        center_y = sum(y_coords) / len(y_coords)
        return center_x, center_y

    def recognize(self, lm_list, frame_width, frame_height):
        """
        Recognizes gestures from hand landmarks and controls the mouse.
        lm_list: List of landmark coordinates [id, x, y, z].
        frame_width, frame_height: Dimensions of the camera frame.
        """
        if not lm_list or len(lm_list) < 21:
            # No hand detected or insufficient landmarks, revert to idle or do nothing
            if self.current_gesture != GESTURE_IDLE and (time.time() - self.last_gesture_time > self.idle_timeout):
                print("No hand, transitioning to IDLE")
                self.current_gesture = GESTURE_IDLE
            return self.current_gesture

        fingers = self.hand_tracker.fingers_up(lm_list)
        # Thumb, Index, Middle, Ring, Pinky
        # print(f"Fingers: {fingers}")

        # Calculate distances for pinch gestures
        # For flipped image: thumb tip (4), index tip (8), middle tip (12), pinky tip (20), pinky mcp (17)
        dist_thumb_index = self.hand_tracker.calculate_distance(lm_list, self.mp_hands.HandLandmark.THUMB_TIP, self.mp_hands.HandLandmark.INDEX_FINGER_TIP)
        dist_thumb_middle = self.hand_tracker.calculate_distance(lm_list, self.mp_hands.HandLandmark.THUMB_TIP, self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP)
        dist_pinky_thumb_base = self.hand_tracker.calculate_distance(lm_list, self.mp_hands.HandLandmark.PINKY_TIP, self.mp_hands.HandLandmark.WRIST) # lm_list[0] is wrist, use its ID
        dist_index_middle_base = self.hand_tracker.calculate_distance(lm_list, self.mp_hands.HandLandmark.INDEX_FINGER_MCP, self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP)

        # --- Gesture Logic ---
        now = time.time()
        action_performed_this_frame = False

        # 1. Left Click: Index finger and Thumb pinch
        if dist_thumb_index < self.pinch_threshold_click and (now - self.last_click_time > self.click_debounce_time):
            if fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]: # Index up, others down (approx)
                self.mouse_controller.left_click()
                self.last_click_time = now
                self.current_gesture = GESTURE_LEFT_CLICK_ACTION
                print(f"Gesture: Left Click (Thumb-Index Pinch: {dist_thumb_index:.3f})")
                action_performed_this_frame = True
        
        # 2. Right Click: Middle finger and Thumb pinch
        elif dist_thumb_middle < self.pinch_threshold_click and (now - self.last_click_time > self.click_debounce_time):
            if fingers[2] and not fingers[1] and not fingers[3] and not fingers[4]: # Middle up, others down (approx)
                self.mouse_controller.right_click()
                self.last_click_time = now
                self.current_gesture = GESTURE_RIGHT_CLICK_ACTION
                print(f"Gesture: Right Click (Thumb-Middle Pinch: {dist_thumb_middle:.3f})")
                action_performed_this_frame = True

        # 3. Scroll Mode: Pinky and Thumb pinch (or specific finger pose)
        # Let's use: Pinky up, other three main fingers down, thumb can be anywhere (or also down)
        elif fingers[4] and not fingers[1] and not fingers[2] and not fingers[3] and (now - self.last_scroll_time > self.scroll_debounce_time):
            if self.current_gesture != GESTURE_SCROLL_READY and self.current_gesture != GESTURE_SCROLL_UP_ACTION and self.current_gesture != GESTURE_SCROLL_DOWN_ACTION:
                self.current_gesture = GESTURE_SCROLL_READY
                self.scroll_ref_y = lm_list[self.mp_hands.HandLandmark.PINKY_TIP][2] # Pinky tip Y as reference
                print(f"Gesture: Scroll Ready (Pinky up, ref_y: {self.scroll_ref_y:.3f})")
                action_performed_this_frame = True
            
            if self.current_gesture == GESTURE_SCROLL_READY or self.current_gesture == GESTURE_SCROLL_UP_ACTION or self.current_gesture == GESTURE_SCROLL_DOWN_ACTION:
                current_pinky_y = lm_list[self.mp_hands.HandLandmark.PINKY_TIP][2]
                delta_y = current_pinky_y - self.scroll_ref_y

                if delta_y > self.scroll_sensitivity: # Pinky moved down (scroll down)
                    self.mouse_controller.scroll(1) # pynput: positive for scroll down
                    self.scroll_ref_y = current_pinky_y # Update reference to allow continuous scroll
                    self.last_scroll_time = now
                    self.current_gesture = GESTURE_SCROLL_DOWN_ACTION
                    print(f"Gesture: Scroll Down (Pinky Y: {current_pinky_y:.3f}, Delta: {delta_y:.3f})")
                    action_performed_this_frame = True
                elif delta_y < -self.scroll_sensitivity: # Pinky moved up (scroll up)
                    self.mouse_controller.scroll(-1) # pynput: negative for scroll up
                    self.scroll_ref_y = current_pinky_y # Update reference
                    self.last_scroll_time = now
                    self.current_gesture = GESTURE_SCROLL_UP_ACTION
                    print(f"Gesture: Scroll Up (Pinky Y: {current_pinky_y:.3f}, Delta: {delta_y:.3f})")
                    action_performed_this_frame = True

        # 4. Mouse Movement: Index finger up, other fingers down (or more relaxed pose)
        # This should be the default if no other specific gesture is detected.
        elif fingers[0] and fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]: # Thumb and Index up (L shape)
            # Use index finger tip for cursor control
            cursor_x_norm = lm_list[self.mp_hands.HandLandmark.INDEX_FINGER_TIP][1]
            cursor_y_norm = lm_list[self.mp_hands.HandLandmark.INDEX_FINGER_TIP][2]
            self.mouse_controller.move_mouse(cursor_x_norm, cursor_y_norm, frame_width, frame_height)
            self.current_gesture = GESTURE_MOVE
            # print(f"Gesture: Move (Index: {cursor_x_norm:.2f}, {cursor_y_norm:.2f})")
            action_performed_this_frame = True # Moving is an action
        
        # 5. Idle: All fingers relatively open, or specific resting pose (e.g. flat hand)
        # For now, if no other gesture is active for a while, or if hand is very still.
        # A simple idle: if all 5 fingers are up (open hand)
        elif all(fingers):
            if self.current_gesture != GESTURE_IDLE:
                 print("Gesture: Transitioning to IDLE (Open Hand)")
            self.current_gesture = GESTURE_IDLE
            # No mouse action for idle, but we mark it as a recognized state
            action_performed_this_frame = True 

        # If no specific action was performed, but hand is present, consider it MOVE or IDLE based on last state
        if not action_performed_this_frame and (self.current_gesture not in [GESTURE_MOVE, GESTURE_IDLE]):
            # If it was a click or scroll, and now it's not, transition to move/idle
            if (now - self.last_gesture_time > self.idle_timeout / 2): # Quicker transition after action
                # Default to move if hand is generally open-ish
                if fingers[1]: # If index is up, assume move intent
                    self.current_gesture = GESTURE_MOVE
                    # Recalculate hand center for movement if needed, or use index finger tip
                    cursor_x_norm = lm_list[self.mp_hands.HandLandmark.INDEX_FINGER_TIP][1]
                    cursor_y_norm = lm_list[self.mp_hands.HandLandmark.INDEX_FINGER_TIP][2]
                    self.mouse_controller.move_mouse(cursor_x_norm, cursor_y_norm, frame_width, frame_height)
                else:
                    self.current_gesture = GESTURE_IDLE
                print(f"Gesture: Post-action transition to {self.current_gesture}")
        
        elif not action_performed_this_frame and self.current_gesture == GESTURE_IDLE:
            # If currently idle, but hand moves significantly, switch to MOVE
            # This part needs more robust logic for "resting hand on table"
            # For now, any detected hand not in another gesture will default to MOVE if index is up
            if fingers[1]: # If index is up, assume move intent
                self.current_gesture = GESTURE_MOVE
                cursor_x_norm = lm_list[self.mp_hands.HandLandmark.INDEX_FINGER_TIP][1]
                cursor_y_norm = lm_list[self.mp_hands.HandLandmark.INDEX_FINGER_TIP][2]
                self.mouse_controller.move_mouse(cursor_x_norm, cursor_y_norm, frame_width, frame_height)

        if action_performed_this_frame or self.current_gesture != GESTURE_NONE:
            self.last_gesture_time = now

        return self.current_gesture

if __name__ == '__main__':
    # This class is tightly coupled with HandTracker and MouseController,
    # so a standalone test here would be complex. 
    # It's better to test it via main.py.
    print("GestureRecognizer class defined. Test via main.py.")
    # mc = MouseController() # Mock or actual
    # ht = HandTracker() # Mock or actual
    # gr = GestureRecognizer(mc, ht)
    # print("GestureRecognizer initialized.")
