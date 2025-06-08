"""
Test script for camera selection functionality
Tests both console and GUI camera selectors
"""

import os
import sys
import time
import subprocess

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import cv2
        print("✓ OpenCV imported successfully")
    except ImportError as e:
        print(f"✗ OpenCV import failed: {e}")
        return False
    
    try:
        from camera_selector import CameraSelector
        print("✓ Console camera selector imported successfully")
    except ImportError as e:
        print(f"✗ Console camera selector import failed: {e}")
        return False
    
    try:
        import tkinter
        print("✓ Tkinter imported successfully")
    except ImportError as e:
        print(f"✗ Tkinter import failed: {e}")
        return False
    
    try:
        from PIL import Image, ImageTk
        print("✓ PIL imported successfully")
    except ImportError as e:
        print(f"✗ PIL import failed: {e}")
        return False
    
    try:
        from camera_selector_gui import CameraSelectorGUI
        print("✓ GUI camera selector imported successfully")
    except ImportError as e:
        print(f"✗ GUI camera selector import failed: {e}")
        return False
    
    return True

def test_camera_detection():
    """Test camera detection functionality"""
    print("\nTesting camera detection...")
    
    try:
        from camera_selector import CameraSelector
        selector = CameraSelector()
        
        print(f"Found {len(selector.available_cameras)} camera(s):")
        for cam in selector.available_cameras:
            print(f"  - Camera {cam['index']}: {cam['width']}x{cam['height']}")
        
        return len(selector.available_cameras) > 0
        
    except Exception as e:
        print(f"✗ Camera detection failed: {e}")
        return False

def test_camera_initialization():
    """Test camera initialization"""
    print("\nTesting camera initialization...")
    
    try:
        import cv2
        
        # Find available cameras
        available_cameras = []
        for i in range(5):  # Check first 5 cameras
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    available_cameras.append(i)
                    print(f"✓ Camera {i} initialized successfully")
                cap.release()
        
        if available_cameras:
            print(f"✓ Successfully initialized {len(available_cameras)} camera(s)")
            return True
        else:
            print("✗ No cameras could be initialized")
            return False
            
    except Exception as e:
        print(f"✗ Camera initialization failed: {e}")
        return False

def test_file_operations():
    """Test camera selection file saving/loading"""
    print("\nTesting file operations...")
    
    try:
        # Test saving camera selection
        test_camera_index = 0
        with open('test_camera_selection.txt', 'w') as f:
            f.write(str(test_camera_index))
        print("✓ Camera selection saved successfully")
        
        # Test loading camera selection
        with open('test_camera_selection.txt', 'r') as f:
            loaded_index = int(f.read().strip())
        
        if loaded_index == test_camera_index:
            print("✓ Camera selection loaded successfully")
        else:
            print("✗ Camera selection loading mismatch")
            return False
        
        # Cleanup
        os.remove('test_camera_selection.txt')
        print("✓ Test file cleanup successful")
        
        return True
        
    except Exception as e:
        print(f"✗ File operations failed: {e}")
        return False

def test_main_integration():
    """Test integration with main.py"""
    print("\nTesting main.py integration...")
    
    try:
        # Create a test camera selection file
        with open('selected_camera.txt', 'w') as f:
            f.write('0')  # Use camera 0
        
        # Test importing main module
        from main import load_selected_camera
        
        # Test loading function
        selected = load_selected_camera()
        if selected == 0:
            print("✓ Main.py integration successful")
            result = True
        else:
            print("✗ Main.py integration failed - wrong camera loaded")
            result = False
        
        # Cleanup
        if os.path.exists('selected_camera.txt'):
            os.remove('selected_camera.txt')
        
        return result
        
    except Exception as e:
        print(f"✗ Main.py integration failed: {e}")
        return False

def run_comprehensive_test():
    """Run all tests"""
    print("=" * 60)
    print("CAMERA SELECTION FUNCTIONALITY TEST")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Camera Detection", test_camera_detection),
        ("Camera Initialization", test_camera_initialization),
        ("File Operations", test_file_operations),
        ("Main Integration", test_main_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 20)
        
        try:
            if test_func():
                print(f"✓ {test_name} PASSED")
                passed += 1
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"TEST SUMMARY: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("🎉 All tests passed! Camera selection functionality is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

def interactive_test():
    """Interactive test mode"""
    print("\n" + "=" * 60)
    print("INTERACTIVE TEST MODE")
    print("=" * 60)
    
    print("\nAvailable interactive tests:")
    print("1. Test console camera selector")
    print("2. Test GUI camera selector (if available)")
    print("3. Test launcher integration")
    print("4. Run all automatic tests")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                print("\nTesting console camera selector...")
                try:
                    from camera_selector import main as console_main
                    console_main()
                except Exception as e:
                    print(f"Console selector test failed: {e}")
            
            elif choice == '2':
                print("\nTesting GUI camera selector...")
                try:
                    from camera_selector_gui import main as gui_main
                    gui_main()
                except Exception as e:
                    print(f"GUI selector test failed: {e}")
            
            elif choice == '3':
                print("\nTesting launcher integration...")
                try:
                    from launcher import main as launcher_main
                    launcher_main()
                except Exception as e:
                    print(f"Launcher test failed: {e}")
            
            elif choice == '4':
                run_comprehensive_test()
            
            elif choice == '5':
                print("Exiting interactive test mode.")
                break
            
            else:
                print("Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\nExiting interactive test mode.")
            break
        except Exception as e:
            print(f"Error in interactive mode: {e}")

def main():
    """Main test function"""
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_test()
    else:
        run_comprehensive_test()

if __name__ == "__main__":
    main()
