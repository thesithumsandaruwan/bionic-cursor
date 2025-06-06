import cv2
import time
import config

class UIManager:
    def __init__(self):
        self.start_time = time.time()
        self.show_instructions = config.SHOW_INSTRUCTIONS
        self.instructions_timeout = config.INSTRUCTIONS_TIMEOUT
        
    def draw_instructions(self, image):
        """Draw instruction overlay on the image"""
        if not self.show_instructions:
            return image
            
        # Check if we should still show instructions
        elapsed_time = time.time() - self.start_time
        if elapsed_time > self.instructions_timeout:
            self.show_instructions = False
            return image
            
        h, w = image.shape[:2]
        
        # Create semi-transparent overlay
        overlay = image.copy()
        cv2.rectangle(overlay, (10, 10), (w-10, h-10), config.COLOR_BLACK, -1)
        image = cv2.addWeighted(image, 0.3, overlay, 0.7, 0)
        
        instructions = [
            "HAND GESTURE MOUSE CONTROL",
            "",
            "GESTURES:",
            "• Move cursor: Point with index finger (L-shape)",
            "• Left click: Pinch thumb + index finger",
            "• Right click: Pinch thumb + middle finger", 
            "• Scroll: Raise pinky, move up/down",
            "• Idle: Open palm (all fingers up)",
            "",
            "CONTROLS:",
            "• 'q' - Quit application",
            "• 'c' - Change camera",
            "• 'i' - Toggle instructions",
            "• 'h' - Show help again",
            "",
            f"Instructions will hide in {int(self.instructions_timeout - elapsed_time)}s"
        ]
        
        y_offset = 50
        for line in instructions:
            if line.startswith("HAND GESTURE") or line.startswith("GESTURES:") or line.startswith("CONTROLS:"):
                color = config.COLOR_YELLOW
                thickness = 2
            elif line.startswith("•"):
                color = config.COLOR_WHITE
                thickness = 1
            else:
                color = config.COLOR_WHITE  
                thickness = 1
                
            cv2.putText(image, line, (30, y_offset), config.FONT, config.FONT_SCALE, color, thickness)
            y_offset += 25
            
        return image
    
    def draw_status_info(self, image, fps, current_gesture, camera_index, gesture_recognizer):
        """Draw FPS, gesture status, and other info"""
        h, w = image.shape[:2]
        
        if config.FPS_DISPLAY:
            cv2.putText(image, f"FPS: {int(fps)}", (10, 30), config.FONT, config.FONT_SCALE, config.COLOR_GREEN, config.FONT_THICKNESS)
        
        if config.GESTURE_DISPLAY:
            # Choose color based on gesture
            if current_gesture == "idle":
                color = config.COLOR_WHITE
            elif "click" in current_gesture:
                color = config.COLOR_RED
            elif "scroll" in current_gesture:
                color = config.COLOR_BLUE
            elif current_gesture == "move":
                color = config.COLOR_GREEN
            else:
                color = config.COLOR_YELLOW
                
            cv2.putText(image, f"Gesture: {current_gesture}", (10, 60), config.FONT, config.FONT_SCALE, color, config.FONT_THICKNESS)
        
        # Camera info
        cv2.putText(image, f"Camera: {camera_index}", (10, 90), config.FONT, config.FONT_SCALE, config.COLOR_WHITE, 1)
        
        # Control hints (bottom of screen)
        control_text = "Controls: 'q'-Quit | 'c'-Camera | 'i'-Instructions | 'h'-Help"
        text_size = cv2.getTextSize(control_text, config.FONT, 0.4, 1)[0]
        cv2.putText(image, control_text, (10, h-10), config.FONT, 0.4, config.COLOR_YELLOW, 1)
        
        return image
    
    def draw_hand_info(self, image, lm_list, fingers):
        """Draw additional hand information for debugging"""
        if not lm_list:
            return image
            
        h, w = image.shape[:2]
        
        # Draw finger status
        finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
        y_start = h - 150
        
        for i, (name, status) in enumerate(zip(finger_names, fingers)):
            color = config.COLOR_GREEN if status else config.COLOR_RED
            text = f"{name}: {'UP' if status else 'DOWN'}"
            cv2.putText(image, text, (w-150, y_start + i*20), config.FONT, 0.4, color, 1)
            
        return image
    
    def toggle_instructions(self):
        """Toggle instruction display"""
        self.show_instructions = not self.show_instructions
        if self.show_instructions:
            self.start_time = time.time()  # Reset timer
    
    def show_help(self):
        """Show instructions again"""
        self.show_instructions = True
        self.start_time = time.time()

class CameraManager:
    def __init__(self):
        self.current_camera = config.DEFAULT_CAMERA_INDEX
        self.available_cameras = self.find_available_cameras()
        self.cap = None
        
    def find_available_cameras(self):
        """Find all available cameras"""
        available = []
        for i in range(10):  # Check first 10 camera indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available.append(i)
                cap.release()
        return available
    
    def initialize_camera(self, camera_index=None):
        """Initialize camera with given index"""
        if camera_index is not None:
            self.current_camera = camera_index
            
        if self.cap:
            self.cap.release()
            
        self.cap = cv2.VideoCapture(self.current_camera)
        if self.cap.isOpened():
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
            return True
        return False
    
    def switch_camera(self):
        """Switch to next available camera"""
        if len(self.available_cameras) <= 1:
            print("Only one camera available")
            return False
            
        current_idx = self.available_cameras.index(self.current_camera) if self.current_camera in self.available_cameras else 0
        next_idx = (current_idx + 1) % len(self.available_cameras)
        next_camera = self.available_cameras[next_idx]
        
        print(f"Switching from camera {self.current_camera} to camera {next_camera}")
        
        if self.initialize_camera(next_camera):
            print(f"Successfully switched to camera {next_camera}")
            return True
        else:
            print(f"Failed to switch to camera {next_camera}")
            return False
    
    def read_frame(self):
        """Read frame from current camera"""
        if self.cap and self.cap.isOpened():
            return self.cap.read()
        return False, None
    
    def release(self):
        """Release camera resources"""
        if self.cap:
            self.cap.release()
    
    def get_camera_info(self):
        """Get current camera information"""
        if self.cap and self.cap.isOpened():
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            return {
                'index': self.current_camera,
                'width': width,
                'height': height,
                'available': self.available_cameras
            }
        return None
