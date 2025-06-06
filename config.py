# Configuration file for Hand Gesture Mouse Control

# Camera settings
DEFAULT_CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Hand tracking settings
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.5
MAX_NUM_HANDS = 1

# Gesture recognition thresholds
PINCH_THRESHOLD_CLICK = 0.06
SCROLL_PINCH_THRESHOLD = 0.07
SCROLL_SENSITIVITY = 0.1

# Timing settings (in seconds)
CLICK_DEBOUNCE_TIME = 0.3
SCROLL_DEBOUNCE_TIME = 0.2
IDLE_TIMEOUT = 1.0
MIN_MOVEMENT_FOR_CURSOR = 0.01

# UI settings
SHOW_INSTRUCTIONS = True
INSTRUCTIONS_TIMEOUT = 10.0  # seconds to show instructions at startup
FPS_DISPLAY = True
GESTURE_DISPLAY = True

# Colors (BGR format for OpenCV)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_BLUE = (255, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_YELLOW = (0, 255, 255)

# Font settings
FONT = 0  # cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.6
FONT_THICKNESS = 2
