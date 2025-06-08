import cv2
import time

class CameraSelector:
    def __init__(self):
        self.available_cameras = self.find_available_cameras()
        self.selected_camera = None
        
    def find_available_cameras(self):
        """Find all available cameras"""
        print("Scanning for available cameras...")
        available = []
        
        for i in range(10):  # Check first 10 camera indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                # Test if we can actually read from the camera
                ret, frame = cap.read()
                if ret and frame is not None:
                    # Get camera information
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    
                    camera_info = {
                        'index': i,
                        'width': width,
                        'height': height,
                        'name': f"Camera {i}"
                    }
                    available.append(camera_info)
                    print(f"Found Camera {i}: {width}x{height}")
                cap.release()
                
        return available
    
    def show_camera_preview(self, camera_info):
        """Show live preview of a specific camera"""
        cap = cv2.VideoCapture(camera_info['index'])
        if not cap.isOpened():
            return False
            
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print(f"\nPreviewing {camera_info['name']} ({camera_info['width']}x{camera_info['height']})")
        print("Press SPACE to select this camera, ESC to go back, or wait 5 seconds to auto-select")
        
        start_time = time.time()
        selected = False
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Add overlay text
            frame_height, frame_width = frame.shape[:2]
            
            # Semi-transparent overlay for text
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (frame_width, 100), (0, 0, 0), -1)
            frame = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)
            
            # Camera info
            cv2.putText(frame, f"Camera {camera_info['index']}: {camera_info['width']}x{camera_info['height']}", 
                       (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Instructions
            cv2.putText(frame, "SPACE: Select  |  ESC: Back  |  Auto-select in:", 
                       (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Countdown
            elapsed = time.time() - start_time
            remaining = max(0, 5 - elapsed)
            cv2.putText(frame, f"{remaining:.1f}s", 
                       (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            cv2.imshow("Camera Preview", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):  # Space key
                selected = True
                break
            elif key == 27:  # ESC key
                break
            elif elapsed >= 5:  # Auto-select after 5 seconds
                selected = True
                break
                
        cap.release()
        cv2.destroyAllWindows()
        return selected
    
    def select_camera(self):
        """Main camera selection interface"""
        if not self.available_cameras:
            print("No cameras found! Please make sure a camera is connected.")
            return None
            
        print(f"\nFound {len(self.available_cameras)} camera(s):")
        for i, cam in enumerate(self.available_cameras):
            print(f"  {i+1}. {cam['name']} - {cam['width']}x{cam['height']}")
        
        if len(self.available_cameras) == 1:
            # Only one camera available
            print(f"\nOnly one camera available. Using {self.available_cameras[0]['name']}")
            if self.show_camera_preview(self.available_cameras[0]):
                self.selected_camera = self.available_cameras[0]['index']
                return self.selected_camera
            else:
                return None
        
        # Multiple cameras available
        while True:
            print(f"\nSelect camera (1-{len(self.available_cameras)}) or 'q' to quit:")
            choice = input("Enter your choice: ").strip().lower()
            
            if choice == 'q':
                return None
                
            try:
                camera_idx = int(choice) - 1
                if 0 <= camera_idx < len(self.available_cameras):
                    camera_info = self.available_cameras[camera_idx]
                    if self.show_camera_preview(camera_info):
                        self.selected_camera = camera_info['index']
                        return self.selected_camera
                    # If not selected, continue the loop
                else:
                    print(f"Invalid choice. Please enter 1-{len(self.available_cameras)}")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def get_selected_camera(self):
        """Get the currently selected camera index"""
        return self.selected_camera

def main():
    """Standalone camera selection tool"""
    print("=" * 50)
    print("HAND GESTURE MOUSE CONTROL - CAMERA SELECTOR")
    print("=" * 50)
    
    selector = CameraSelector()
    selected_camera = selector.select_camera()
    
    if selected_camera is not None:
        print(f"\nCamera {selected_camera} selected successfully!")
        print("You can now run the main application with this camera.")
        
        # Save selection to a file for the main program to use
        try:
            with open('selected_camera.txt', 'w') as f:
                f.write(str(selected_camera))
            print("Camera selection saved.")
        except Exception as e:
            print(f"Warning: Could not save camera selection: {e}")
        
        return selected_camera
    else:
        print("\nNo camera selected. Exiting.")
        return None

if __name__ == "__main__":
    main()
