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
        
        # Smoothing for mouse movement
        self.prev_cursor_x = None
        self.prev_cursor_y = None
        self.smoothing_factor = 0.7  # Higher = smoother but slower response
        
        # Gesture state tracking
        self.gesture_start_time = time.time()
        self.gesture_hold_time = 0.1  # Time to hold gesture before action
        
        # Click state tracking
        self.left_click_prepared = False
        self.right_click_prepared = False
        self.left_click_start_time = 0
        self.right_click_start_time = 0

        # Load thresholds from config
        self.pinch_threshold_click = config.PINCH_THRESHOLD_CLICK
        self.scroll_pinch_threshold = config.SCROLL_PINCH_THRESHOLD
        self.scroll_sensitivity = config.SCROLL_SENSITIVITY
        self.click_debounce_time = config.CLICK_DEBOUNCE_TIME
        self.scroll_debounce_time = config.SCROLL_DEBOUNCE_TIME
        self.idle_timeout = config.IDLE_TIMEOUT

        # Scroll gesture parameters
        self.scroll_ref_y = None # Y-coordinate of pinky base when scroll gesture starts
        self.in_scroll_mode = False

    def _calculate_hand_center(self, lm_list):
        if not lm_list or len(lm_list) < 21:
            return None, None
        # Use wrist (0) and MCP of middle finger (9) as a simple center proxy
        x_coords = [lm_list[0][1], lm_list[9][1]]
        y_coords = [lm_list[0][2], lm_list[9][2]]
        center_x = sum(x_coords) / len(x_coords)
        center_y = sum(y_coords) / len(y_coords)
        return center_x, center_y
    
    def _smooth_cursor_movement(self, target_x, target_y):
        """Apply smoothing to cursor movement for better user experience"""
        if self.prev_cursor_x is None or self.prev_cursor_y is None:
            self.prev_cursor_x = target_x
            self.prev_cursor_y = target_y
            return target_x, target_y
        
        # Apply exponential smoothing
        smooth_x = self.prev_cursor_x + (target_x - self.prev_cursor_x) * (1 - self.smoothing_factor)
        smooth_y = self.prev_cursor_y + (target_y - self.prev_cursor_y) * (1 - self.smoothing_factor)
        
        self.prev_cursor_x = smooth_x
        self.prev_cursor_y = smooth_y
        
        return smooth_x, smooth_y
    
    def _is_gesture_stable(self, current_time, required_hold_time=None):
        """Check if current gesture has been held long enough to be considered stable"""
        if required_hold_time is None:
            required_hold_time = self.gesture_hold_time
        return (current_time - self.gesture_start_time) >= required_hold_time

    def recognize(self, lm_list, frame_width, frame_height):
        """
        Recognizes gestures from hand landmarks and controls the mouse.
        lm_list: List of landmark coordinates [id, x, y, z].
        frame_width, frame_height: Dimensions of the camera frame.
        """
        if not lm_list or len(lm_list) < 21:
            # No hand detected or insufficient landmarks
            if self.current_gesture != GESTURE_IDLE:
                self.current_gesture = GESTURE_IDLE
                self.in_scroll_mode = False
                # Reset smoothing when hand disappears
                self.prev_cursor_x = None
                self.prev_cursor_y = None
            return self.current_gesture

        fingers = self.hand_tracker.fingers_up(lm_list)
        now = time.time()
        
        # Calculate distances for pinch gestures
        dist_thumb_index = self.hand_tracker.calculate_distance(
            lm_list, 
            self.mp_hands.HandLandmark.THUMB_TIP, 
            self.mp_hands.HandLandmark.INDEX_FINGER_TIP
        )
        dist_thumb_ring = self.hand_tracker.calculate_distance(
            lm_list, 
            self.mp_hands.HandLandmark.THUMB_TIP, 
            self.mp_hands.HandLandmark.RING_FINGER_TIP
        )
        
        # --- Gesture Priority Logic ---
        
        # 1. IDLE STATE: All fingers up (open palm) - highest priority for safety
        if all(fingers):
            if self.current_gesture != GESTURE_IDLE:
                self.current_gesture = GESTURE_IDLE
                self.in_scroll_mode = False
                print("Gesture: IDLE (Open Palm)")
            return self.current_gesture
        
        # 2. LEFT CLICK: Thumb and index pinch (other fingers can be up or down)
        if dist_thumb_index < self.pinch_threshold_click:
            if not self.left_click_prepared:
                self.left_click_prepared = True
                self.left_click_start_time = now
                self.current_gesture = GESTURE_LEFT_CLICK_READY
                print(f"Gesture: Left Click Ready (Distance: {dist_thumb_index:.3f})")
            elif (now - self.left_click_start_time > self.gesture_hold_time and 
                  now - self.last_click_time > self.click_debounce_time):
                self.mouse_controller.left_click()
                self.last_click_time = now
                self.current_gesture = GESTURE_LEFT_CLICK_ACTION
                self.left_click_prepared = False
                print(f"Gesture: LEFT CLICK EXECUTED")
            return self.current_gesture
        else:
            self.left_click_prepared = False
        
        # 3. RIGHT CLICK: Thumb and ring finger pinch (index and middle should be up)
        if (dist_thumb_ring < self.pinch_threshold_click and 
            fingers[1] and fingers[2]):  # Index and middle fingers should be up for right click
            if not self.right_click_prepared:
                self.right_click_prepared = True
                self.right_click_start_time = now
                self.current_gesture = GESTURE_RIGHT_CLICK_READY
                print(f"Gesture: Right Click Ready (Distance: {dist_thumb_ring:.3f})")
            elif (now - self.right_click_start_time > self.gesture_hold_time and 
                  now - self.last_click_time > self.click_debounce_time):
                self.mouse_controller.right_click()
                self.last_click_time = now
                self.current_gesture = GESTURE_RIGHT_CLICK_ACTION
                self.right_click_prepared = False
                print(f"Gesture: RIGHT CLICK EXECUTED")
            return self.current_gesture
        else:
            self.right_click_prepared = False
        
        # 4. SCROLL MODE: Only pinky up, all others down
        if (fingers[4] and not fingers[1] and not fingers[2] and not fingers[3]):
            if not self.in_scroll_mode:
                self.in_scroll_mode = True
                self.scroll_ref_y = lm_list[self.mp_hands.HandLandmark.PINKY_TIP][2]
                self.current_gesture = GESTURE_SCROLL_READY
                print(f"Gesture: Scroll Mode Activated (Ref Y: {self.scroll_ref_y:.3f})")
            else:
                # We're in scroll mode, check for movement
                current_pinky_y = lm_list[self.mp_hands.HandLandmark.PINKY_TIP][2]
                delta_y = current_pinky_y - self.scroll_ref_y
                
                if (abs(delta_y) > self.scroll_sensitivity and 
                    now - self.last_scroll_time > self.scroll_debounce_time):
                    
                    if delta_y > 0:  # Pinky moved down -> scroll down
                        self.mouse_controller.scroll(1)
                        self.current_gesture = GESTURE_SCROLL_DOWN_ACTION
                        print(f"Gesture: SCROLL DOWN (Delta: {delta_y:.3f})")
                    else:  # Pinky moved up -> scroll up
                        self.mouse_controller.scroll(-1)
                        self.current_gesture = GESTURE_SCROLL_UP_ACTION
                        print(f"Gesture: SCROLL UP (Delta: {delta_y:.3f})")
                    
                    self.scroll_ref_y = current_pinky_y  # Update reference
                    self.last_scroll_time = now
            return self.current_gesture
        else:
            self.in_scroll_mode = False
        
        # 5. MOUSE MOVEMENT: Index finger up (L-shape with thumb) or just index up
        if fingers[1]:  # Index finger is up
            # Use index finger tip for cursor control
            cursor_x_norm = lm_list[self.mp_hands.HandLandmark.INDEX_FINGER_TIP][1]
            cursor_y_norm = lm_list[self.mp_hands.HandLandmark.INDEX_FINGER_TIP][2]
            
            # Apply smoothing
            smooth_x, smooth_y = self._smooth_cursor_movement(cursor_x_norm, cursor_y_norm)
            
            # Move mouse with smoothed coordinates
            self.mouse_controller.move_mouse(smooth_x, smooth_y, frame_width, frame_height)
            self.current_gesture = GESTURE_MOVE
            # Uncomment for debugging: print(f"Gesture: MOVE (Smooth: {smooth_x:.3f}, {smooth_y:.3f})")
            return self.current_gesture
        
        # 6. DEFAULT: If no specific gesture detected, remain in current state or go idle
        if self.current_gesture not in [GESTURE_IDLE, GESTURE_MOVE]:
            # Transition from action states back to move or idle
            if fingers[1]:  # If index is still up, go to move
                self.current_gesture = GESTURE_MOVE
            else:
                self.current_gesture = GESTURE_IDLE
                print("Gesture: Transitioning to IDLE")
        
        self.last_gesture_time = now
        return self.current_gesture

    def get_gesture_info(self):
        """Get current gesture information for UI display"""
        return {
            'current_gesture': self.current_gesture,
            'left_click_prepared': self.left_click_prepared,
            'right_click_prepared': self.right_click_prepared,
            'in_scroll_mode': self.in_scroll_mode,
            'smoothing_factor': self.smoothing_factor
        }
    
    def reset_gesture_state(self):
        """Reset all gesture states - useful for recalibration"""
        self.current_gesture = GESTURE_IDLE
        self.left_click_prepared = False
        self.right_click_prepared = False
        self.in_scroll_mode = False
        self.prev_cursor_x = None
        self.prev_cursor_y = None
        print("Gesture state reset to IDLE")

if __name__ == '__main__':
    # This class is tightly coupled with HandTracker and MouseController,
    # so a standalone test here would be complex. 
    # It's better to test it via main.py.
    print("GestureRecognizer class defined. Test via main.py.")
    # mc = MouseController() # Mock or actual
    # ht = HandTracker() # Mock or actual
    # gr = GestureRecognizer(mc, ht)
    # print("GestureRecognizer initialized.")
