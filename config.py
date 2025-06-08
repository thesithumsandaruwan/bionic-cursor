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
PINCH_THRESHOLD_CLICK = 0.04  # Reduced for more sensitive click detection
SCROLL_PINCH_THRESHOLD = 0.07
SCROLL_SENSITIVITY = 0.05  # Reduced for more responsive scrolling

# Timing settings (in seconds)
CLICK_DEBOUNCE_TIME = 0.5  # Increased to prevent accidental double clicks
SCROLL_DEBOUNCE_TIME = 0.1  # Reduced for smoother scrolling
IDLE_TIMEOUT = 0.5  # Reduced for faster state transitions
MIN_MOVEMENT_FOR_CURSOR = 0.005  # Reduced threshold for movement detection

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
