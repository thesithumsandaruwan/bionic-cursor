import os
import sys
import subprocess
from camera_selector import CameraSelector

def main():
    """Enhanced launcher that first selects camera, then runs main program"""
    print("=" * 60)
    print("HAND GESTURE MOUSE CONTROL - LAUNCHER")
    print("=" * 60)
    print()
    
    # Step 1: Camera Selection
    print("Step 1: Camera Selection")
    print("-" * 25)
    
    selected_camera = None
    
    # Try GUI version first, fallback to console version
    try:
        print("Starting GUI camera selector...")
        from camera_selector_gui import CameraSelectorGUI
        
        app = CameraSelectorGUI()
        selected_camera = app.run()
        
    except Exception as e:
        print(f"GUI selector failed ({e}), using console version...")
        
        from camera_selector import CameraSelector
        selector = CameraSelector()
        selected_camera = selector.select_camera()
    
    if selected_camera is None:
        print("\nNo camera selected. Cannot start application.")
        input("Press Enter to exit...")
        return
    
    print(f"\nCamera {selected_camera} selected successfully!")
    
    # Step 2: Start Main Application
    print("\nStep 2: Starting Main Application")
    print("-" * 35)
    
    # Save the selected camera for the main program
    try:
        with open('selected_camera.txt', 'w') as f:
            f.write(str(selected_camera))
        print("Camera selection saved.")
    except Exception as e:
        print(f"Warning: Could not save camera selection: {e}")
    
    # Import and run the main program
    try:
        print("Loading main application...")
        
        # Import main module
        from main import main as run_main
        
        # Run the main application
        run_main()
        
    except ImportError as e:
        print(f"Error importing main module: {e}")
        print("Make sure all required files are present.")
    except Exception as e:
        print(f"Error running main application: {e}")
        print("Check the console for detailed error information.")
    
    print("\nApplication ended.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
