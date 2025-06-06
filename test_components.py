#!/usr/bin/env python3
"""
Test script to verify the hand gesture mouse control improvements
"""

def test_imports():
    """Test if all modules can be imported"""
    try:
        print("Testing imports...")
        
        # Test config
        import config
        print("✓ config module imported successfully")
        
        # Test mouse controller
        from mouse_controller import MouseController
        print("✓ MouseController imported successfully")
        
        # Test hand tracker
        from hand_tracker import HandTracker
        print("✓ HandTracker imported successfully")
        
        # Test gesture recognizer
        from gesture_recognizer import GestureRecognizer
        print("✓ GestureRecognizer imported successfully")
        
        # Test UI manager
        from ui_manager import UIManager, CameraManager
        print("✓ UIManager and CameraManager imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_config():
    """Test configuration values"""
    try:
        import config
        print(f"\nConfiguration values:")
        print(f"  Camera: {config.CAMERA_WIDTH}x{config.CAMERA_HEIGHT}")
        print(f"  Detection confidence: {config.MIN_DETECTION_CONFIDENCE}")
        print(f"  Click threshold: {config.PINCH_THRESHOLD_CLICK}")
        print(f"  Scroll sensitivity: {config.SCROLL_SENSITIVITY}")
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False

def test_components():
    """Test individual components without camera"""
    try:
        print(f"\nTesting components...")
        
        # Test MouseController
        from mouse_controller import MouseController
        mc = MouseController()
        print(f"✓ MouseController initialized (Screen: {mc.screen_width}x{mc.screen_height})")
        
        # Test HandTracker (without camera)
        from hand_tracker import HandTracker
        ht = HandTracker()
        print("✓ HandTracker initialized")
        
        # Test UIManager
        from ui_manager import UIManager, CameraManager
        ui = UIManager()
        print("✓ UIManager initialized")
        
        # Test CameraManager
        cm = CameraManager()
        print(f"✓ CameraManager initialized (Available cameras: {cm.available_cameras})")
        
        return True
        
    except Exception as e:
        print(f"✗ Component test failed: {e}")
        return False

if __name__ == "__main__":
    print("Hand Gesture Mouse Control - Component Test")
    print("=" * 50)
    
    success = True
    
    # Run tests
    success &= test_imports()
    success &= test_config()
    success &= test_components()
    
    print("\n" + "=" * 50)
    if success:
        print("✓ All tests passed! The application should work correctly.")
        print("\nTo run the full application:")
        print("  python main.py")
        print("\nControls:")
        print("  'q' - Quit")
        print("  'c' - Change camera")
        print("  'i' - Toggle instructions")
        print("  'h' - Show help")
    else:
        print("✗ Some tests failed. Please check the error messages above.")
        print("\nCommon solutions:")
        print("  1. Install dependencies: pip install opencv-python mediapipe pynput")
        print("  2. Make sure you have Python 3.8+")
        print("  3. Check that your camera is not being used by other apps")
    
    print("\n" + "=" * 50)
