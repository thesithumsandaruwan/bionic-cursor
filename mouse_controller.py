from pynput.mouse import Button, Controller
import tkinter as tk
import math

class MouseController:
    def __init__(self):
        self.mouse = Controller()
        try:
            root = tk.Tk()
            self.screen_width = root.winfo_screenwidth()
            self.screen_height = root.winfo_screenheight()
            root.destroy()
        except tk.TclError:
            print("Warning: Could not initialize tkinter to get screen dimensions. Using default 1920x1080.")
            self.screen_width = 1920
            self.screen_height = 1080
        
        # Enhanced smoothing parameters
        self.prev_x, self.prev_y = 0, 0
        self.velocity_x, self.velocity_y = 0, 0
        self.acceleration_factor = 0.8
        self.max_velocity = 50  # pixels per frame
        
        # Movement deadzone to reduce jitter
        self.deadzone_radius = 5  # pixels

    def map_value(self, value, in_min, in_max, out_min, out_max):
        # Ensure no division by zero
        if (in_max - in_min) == 0:
            return out_min
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def move_mouse(self, hand_x, hand_y, frame_width, frame_height, smoothing=True):
        """
        Moves the mouse cursor based on hand coordinates with enhanced smoothing.
        hand_x, hand_y: Normalized coordinates from MediaPipe (0.0 to 1.0)
        frame_width, frame_height: Dimensions of the camera frame.
        """
        # Map hand coordinates to screen coordinates
        # Natural movement: right hand movement = right cursor movement
        target_x = self.map_value(hand_x, 0, 1, 0, self.screen_width)
        target_y = self.map_value(hand_y, 0, 1, 0, self.screen_height)
        
        if smoothing:
            # Calculate movement delta
            delta_x = target_x - self.prev_x
            delta_y = target_y - self.prev_y
            
            # Apply deadzone to reduce jitter
            distance = math.sqrt(delta_x**2 + delta_y**2)
            if distance < self.deadzone_radius:
                return  # Don't move if within deadzone
            
            # Apply acceleration-based smoothing
            self.velocity_x += delta_x * self.acceleration_factor
            self.velocity_y += delta_y * self.acceleration_factor
            
            # Limit maximum velocity to prevent overshooting
            velocity_magnitude = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
            if velocity_magnitude > self.max_velocity:
                scale = self.max_velocity / velocity_magnitude
                self.velocity_x *= scale
                self.velocity_y *= scale
            
            # Apply velocity with damping
            current_x = self.prev_x + self.velocity_x * 0.3
            current_y = self.prev_y + self.velocity_y * 0.3
            
            # Apply additional damping to velocity
            self.velocity_x *= 0.7
            self.velocity_y *= 0.7
            
            # Update position
            self.mouse.position = (int(current_x), int(current_y))
            self.prev_x, self.prev_y = current_x, current_y
        else:
            # Direct mapping without smoothing
            self.mouse.position = (int(target_x), int(target_y))
            self.prev_x, self.prev_y = target_x, target_y


    def left_click(self):
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)
        print("Mouse Action: Left Click")

    def press_left_click(self):
        """Press and hold left mouse button for dragging"""
        self.mouse.press(Button.left)
        print("Mouse Action: Left Press (Drag Start)")

    def release_left_click(self):
        """Release left mouse button to end dragging"""
        self.mouse.release(Button.left)
        print("Mouse Action: Left Release (Drag End)")

    def right_click(self):
        self.mouse.press(Button.right)
        self.mouse.release(Button.right)
        print("Mouse Action: Right Click")

    def scroll(self, dy):
        """
        Scrolls the mouse wheel.
        dy: positive for scroll down, negative for scroll up.
        """
        self.mouse.scroll(0, dy)
        print(f"Mouse Action: Scroll by {dy}")

if __name__ == '__main__':
    # Test functions (optional)
    mc = MouseController()
    print(f"Screen dimensions: {mc.screen_width}x{mc.screen_height}")
    # mc.move_mouse(0.5, 0.5, 640, 480) # Example: move to center of a 640x480 frame
    # time.sleep(1)
    # mc.left_click()
