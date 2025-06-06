from pynput.mouse import Button, Controller
import tkinter as tk

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
        self.prev_x, self.prev_y = 0, 0 # For smoothing (optional)

    def map_value(self, value, in_min, in_max, out_min, out_max):
        # Ensure no division by zero
        if (in_max - in_min) == 0:
            return out_min
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def move_mouse(self, hand_x, hand_y, frame_width, frame_height, smoothing=0.2):
        """
        Moves the mouse cursor based on hand coordinates.
        hand_x, hand_y: Normalized coordinates from MediaPipe (0.0 to 1.0)
        frame_width, frame_height: Dimensions of the camera frame.
        """
        # Map hand coordinates (relative to frame) to screen coordinates
        # Inverting hand_x to make movement more natural if camera is not flipped
        target_x = self.map_value(hand_x, 0, 1, 0, self.screen_width)
        target_y = self.map_value(hand_y, 0, 1, 0, self.screen_height)

        # Optional: Apply smoothing
        # current_x = self.prev_x + (target_x - self.prev_x) * smoothing
        # current_y = self.prev_y + (target_y - self.prev_y) * smoothing
        
        # self.mouse.position = (int(current_x), int(current_y))
        # self.prev_x, self.prev_y = current_x, current_y
        
        # Direct mapping without smoothing for simplicity first
        self.mouse.position = (int(target_x), int(target_y))


    def left_click(self):
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)
        print("Mouse Action: Left Click")

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
