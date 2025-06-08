import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import threading
import time
from PIL import Image, ImageTk
import os

class CameraSelectorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hand Gesture Mouse Control - Camera Selector")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.available_cameras = []
        self.current_preview = None
        self.preview_thread = None
        self.preview_running = False
        self.selected_camera = None
        
        self.setup_ui()
        self.scan_cameras()
        
    def setup_ui(self):
        """Setup the GUI interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Hand Gesture Mouse Control", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, text="Select Your Camera", 
                                  font=("Arial", 12))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Left panel - Camera list
        left_frame = ttk.LabelFrame(main_frame, text="Available Cameras", padding="10")
        left_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Camera listbox
        self.camera_listbox = tk.Listbox(left_frame, height=8)
        self.camera_listbox.pack(fill=tk.BOTH, expand=True)
        self.camera_listbox.bind('<<ListboxSelect>>', self.on_camera_select)
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.refresh_btn = ttk.Button(button_frame, text="Refresh", command=self.scan_cameras)
        self.refresh_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.select_btn = ttk.Button(button_frame, text="Select Camera", 
                                   command=self.select_camera, state=tk.DISABLED)
        self.select_btn.pack(side=tk.LEFT, padx=(5, 5))
        
        self.quit_btn = ttk.Button(button_frame, text="Quit", command=self.quit_application)
        self.quit_btn.pack(side=tk.RIGHT)
        
        # Right panel - Preview
        right_frame = ttk.LabelFrame(main_frame, text="Camera Preview", padding="10")
        right_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Preview canvas
        self.preview_canvas = tk.Canvas(right_frame, width=400, height=300, bg='black')
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Scanning for cameras...", 
                                     font=("Arial", 10))
        self.status_label.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
    def scan_cameras(self):
        """Scan for available cameras"""
        self.status_label.config(text="Scanning for cameras...")
        self.camera_listbox.delete(0, tk.END)
        self.available_cameras = []
        
        # Run scanning in a separate thread to avoid freezing the GUI
        threading.Thread(target=self._scan_cameras_thread, daemon=True).start()
        
    def _scan_cameras_thread(self):
        """Background thread for camera scanning"""
        available = []
        
        for i in range(10):  # Check first 10 camera indices
            try:
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
                            'name': f"Camera {i} ({width}x{height})"
                        }
                        available.append(camera_info)
                    cap.release()
            except Exception as e:
                print(f"Error checking camera {i}: {e}")
                
        # Update GUI in main thread
        self.root.after(0, self._update_camera_list, available)
        
    def _update_camera_list(self, available):
        """Update camera list in main thread"""
        self.available_cameras = available
        
        if not available:
            self.camera_listbox.insert(0, "No cameras found")
            self.status_label.config(text="No cameras found. Check connections.")
        else:
            for cam in available:
                self.camera_listbox.insert(tk.END, cam['name'])
            self.status_label.config(text=f"Found {len(available)} camera(s). Select one to preview.")
            
    def on_camera_select(self, event):
        """Handle camera selection from listbox"""
        selection = self.camera_listbox.curselection()
        if selection and self.available_cameras:
            camera_idx = selection[0]
            if camera_idx < len(self.available_cameras):
                self.start_preview(self.available_cameras[camera_idx])
                self.select_btn.config(state=tk.NORMAL)
            
    def start_preview(self, camera_info):
        """Start camera preview"""
        self.stop_preview()
        self.current_preview = camera_info
        self.preview_running = True
        self.preview_thread = threading.Thread(target=self._preview_thread, daemon=True)
        self.preview_thread.start()
        self.status_label.config(text=f"Previewing {camera_info['name']}")
        
    def stop_preview(self):
        """Stop camera preview"""
        self.preview_running = False
        if self.preview_thread and self.preview_thread.is_alive():
            self.preview_thread.join(timeout=1.0)
        self.preview_canvas.delete("all")
        
    def _preview_thread(self):
        """Background thread for camera preview"""
        if not self.current_preview:
            return
            
        cap = cv2.VideoCapture(self.current_preview['index'])
        if not cap.isOpened():
            self.root.after(0, lambda: self.status_label.config(text="Failed to open camera for preview"))
            return
            
        # Set preview size
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        while self.preview_running:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Convert frame for tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Resize frame to fit canvas
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:  # Canvas is initialized
                frame_height, frame_width = frame_rgb.shape[:2]
                
                # Calculate scaling to fit canvas while maintaining aspect ratio
                scale_w = canvas_width / frame_width
                scale_h = canvas_height / frame_height
                scale = min(scale_w, scale_h)
                
                new_width = int(frame_width * scale)
                new_height = int(frame_height * scale)
                
                # Resize frame
                frame_resized = cv2.resize(frame_rgb, (new_width, new_height))
                
                # Convert to PIL Image
                pil_image = Image.fromarray(frame_resized)
                photo = ImageTk.PhotoImage(pil_image)
                
                # Update canvas in main thread
                self.root.after(0, self._update_preview, photo, new_width, new_height)
                
            time.sleep(0.033)  # ~30 FPS
            
        cap.release()
        
    def _update_preview(self, photo, width, height):
        """Update preview canvas in main thread"""
        if self.preview_running:
            self.preview_canvas.delete("all")
            
            # Center the image on canvas
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            x = (canvas_width - width) // 2
            y = (canvas_height - height) // 2
            
            self.preview_canvas.create_image(x, y, anchor=tk.NW, image=photo)
            # Keep a reference to prevent garbage collection
            self.preview_canvas.image = photo
            
    def select_camera(self):
        """Select the current camera and save selection"""
        if not self.current_preview:
            return
            
        self.selected_camera = self.current_preview['index']
        
        # Save selection to file
        try:
            with open('selected_camera.txt', 'w') as f:
                f.write(str(self.selected_camera))
            
            messagebox.showinfo("Camera Selected", 
                              f"Camera {self.selected_camera} selected successfully!\n"
                              f"Selection saved. You can now run the main application.")
            
            self.quit_application()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not save camera selection: {e}")
            
    def quit_application(self):
        """Quit the application"""
        self.stop_preview()
        self.root.quit()
        self.root.destroy()
        
    def run(self):
        """Run the GUI application"""
        self.root.protocol("WM_DELETE_WINDOW", self.quit_application)
        self.root.mainloop()
        return self.selected_camera

def main():
    """Main function for standalone GUI camera selector"""
    print("Starting GUI Camera Selector...")
    
    try:
        app = CameraSelectorGUI()
        selected_camera = app.run()
        
        if selected_camera is not None:
            print(f"Camera {selected_camera} selected successfully!")
            return selected_camera
        else:
            print("No camera selected.")
            return None
            
    except Exception as e:
        print(f"Error running GUI camera selector: {e}")
        print("Falling back to console version...")
        
        # Fallback to console version
        from camera_selector import CameraSelector
        selector = CameraSelector()
        return selector.select_camera()

if __name__ == "__main__":
    main()
