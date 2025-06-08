"""
Configuration GUI for fine-tuning gesture recognition parameters
Allows real-time adjustment of thresholds and settings
"""

import tkinter as tk
from tkinter import ttk, messagebox
import config
import json
import os

class GestureConfigGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hand Gesture Mouse Control - Configuration")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        # Current configuration values
        self.config_vars = {}
        
        self.setup_ui()
        self.load_current_config()
        
    def setup_ui(self):
        """Setup the configuration GUI"""
        # Main frame with scrollbar
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Gesture Recognition Configuration", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Create notebook for organized sections
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(1, weight=1)
        
        # Gesture Thresholds Tab
        thresholds_frame = ttk.Frame(notebook, padding="10")
        notebook.add(thresholds_frame, text="Gesture Thresholds")
        self.setup_thresholds_tab(thresholds_frame)
        
        # Timing Settings Tab
        timing_frame = ttk.Frame(notebook, padding="10")
        notebook.add(timing_frame, text="Timing Settings")
        self.setup_timing_tab(timing_frame)
        
        # Mouse Control Tab
        mouse_frame = ttk.Frame(notebook, padding="10")
        notebook.add(mouse_frame, text="Mouse Control")
        self.setup_mouse_tab(mouse_frame)
        
        # Camera Settings Tab
        camera_frame = ttk.Frame(notebook, padding="10")
        notebook.add(camera_frame, text="Camera Settings")
        self.setup_camera_tab(camera_frame)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        button_frame.columnconfigure(1, weight=1)
        
        ttk.Button(button_frame, text="Load Defaults", command=self.load_defaults).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="Save & Apply", command=self.save_config).grid(row=0, column=2, padx=(5, 5))
        ttk.Button(button_frame, text="Test Configuration", command=self.test_config).grid(row=0, column=3, padx=(5, 5))
        ttk.Button(button_frame, text="Close", command=self.close_application).grid(row=0, column=4, padx=(5, 0))
        
    def setup_thresholds_tab(self, parent):
        """Setup gesture thresholds configuration"""
        row = 0
        
        # Pinch Thresholds
        ttk.Label(parent, text="Click Detection", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        row += 1
        
        self.add_scale_control(parent, row, "Pinch Threshold (Click)", "PINCH_THRESHOLD_CLICK", 0.01, 0.15, 0.001, 
                              "Lower = more sensitive click detection")
        row += 1
        
        # Scroll Thresholds
        ttk.Label(parent, text="Scroll Detection", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))
        row += 1
        
        self.add_scale_control(parent, row, "Scroll Sensitivity", "SCROLL_SENSITIVITY", 0.01, 0.2, 0.005,
                              "Lower = more sensitive scroll detection")
        row += 1
        
        self.add_scale_control(parent, row, "Scroll Pinch Threshold", "SCROLL_PINCH_THRESHOLD", 0.01, 0.15, 0.001,
                              "Threshold for scroll gesture activation")
        row += 1
        
        # Movement Thresholds
        ttk.Label(parent, text="Movement Detection", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))
        row += 1
        
        self.add_scale_control(parent, row, "Min Movement for Cursor", "MIN_MOVEMENT_FOR_CURSOR", 0.001, 0.05, 0.001,
                              "Minimum movement to trigger cursor update")
        
    def setup_timing_tab(self, parent):
        """Setup timing configuration"""
        row = 0
        
        # Click Timing
        ttk.Label(parent, text="Click Timing", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        row += 1
        
        self.add_scale_control(parent, row, "Click Debounce Time (s)", "CLICK_DEBOUNCE_TIME", 0.1, 1.0, 0.05,
                              "Minimum time between clicks")
        row += 1
        
        # Scroll Timing
        ttk.Label(parent, text="Scroll Timing", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))
        row += 1
        
        self.add_scale_control(parent, row, "Scroll Debounce Time (s)", "SCROLL_DEBOUNCE_TIME", 0.05, 0.5, 0.01,
                              "Minimum time between scroll actions")
        row += 1
        
        # Gesture Timing
        ttk.Label(parent, text="Gesture Timing", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))
        row += 1
        
        self.add_scale_control(parent, row, "Idle Timeout (s)", "IDLE_TIMEOUT", 0.1, 2.0, 0.1,
                              "Time before transitioning to idle state")
        
    def setup_mouse_tab(self, parent):
        """Setup mouse control configuration"""
        row = 0
        
        # Instructions
        ttk.Label(parent, text="Mouse Control Settings", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        row += 1
        
        ttk.Label(parent, text="Note: Mouse control settings will be implemented\nin future versions.", 
                 foreground="gray").grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))
        row += 1
        
        # Placeholder for future mouse settings
        ttk.Label(parent, text="Smoothing Factor: Coming soon").grid(row=row, column=0, sticky=tk.W)
        row += 1
        ttk.Label(parent, text="Acceleration: Coming soon").grid(row=row, column=0, sticky=tk.W)
        row += 1
        ttk.Label(parent, text="Deadzone Radius: Coming soon").grid(row=row, column=0, sticky=tk.W)
        
    def setup_camera_tab(self, parent):
        """Setup camera configuration"""
        row = 0
        
        # Camera Settings
        ttk.Label(parent, text="Camera Settings", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        row += 1
        
        self.add_scale_control(parent, row, "Camera Width", "CAMERA_WIDTH", 320, 1920, 160,
                              "Camera resolution width")
        row += 1
        
        self.add_scale_control(parent, row, "Camera Height", "CAMERA_HEIGHT", 240, 1080, 120,
                              "Camera resolution height")
        row += 1
        
        # Hand Tracking Settings
        ttk.Label(parent, text="Hand Tracking", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))
        row += 1
        
        self.add_scale_control(parent, row, "Min Detection Confidence", "MIN_DETECTION_CONFIDENCE", 0.1, 1.0, 0.05,
                              "Minimum confidence for hand detection")
        row += 1
        
        self.add_scale_control(parent, row, "Min Tracking Confidence", "MIN_TRACKING_CONFIDENCE", 0.1, 1.0, 0.05,
                              "Minimum confidence for hand tracking")
        
    def add_scale_control(self, parent, row, label, config_key, min_val, max_val, resolution, description=""):
        """Add a scale control for configuration parameter"""
        # Label
        ttk.Label(parent, text=label + ":").grid(row=row, column=0, sticky=tk.W, pady=2)
        
        # Variable
        var = tk.DoubleVar()
        self.config_vars[config_key] = var
        
        # Scale
        scale = ttk.Scale(parent, from_=min_val, to=max_val, variable=var, orient=tk.HORIZONTAL)
        scale.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=(10, 10), pady=2)
        parent.columnconfigure(1, weight=1)
        
        # Value label
        value_label = ttk.Label(parent, text="0.000")
        value_label.grid(row=row, column=2, sticky=tk.W, pady=2)
        
        # Update value label when scale changes
        def update_label(*args):
            value_label.config(text=f"{var.get():.3f}")
        var.trace('w', update_label)
        
        # Description
        if description:
            ttk.Label(parent, text=description, foreground="gray", font=("Arial", 8)).grid(
                row=row+1, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
            return row + 2
        
        return row + 1
        
    def load_current_config(self):
        """Load current configuration values"""
        for key, var in self.config_vars.items():
            if hasattr(config, key):
                var.set(getattr(config, key))
                
    def load_defaults(self):
        """Load default configuration values"""
        defaults = {
            'PINCH_THRESHOLD_CLICK': 0.04,
            'SCROLL_SENSITIVITY': 0.05,
            'SCROLL_PINCH_THRESHOLD': 0.07,
            'MIN_MOVEMENT_FOR_CURSOR': 0.005,
            'CLICK_DEBOUNCE_TIME': 0.5,
            'SCROLL_DEBOUNCE_TIME': 0.1,
            'IDLE_TIMEOUT': 0.5,
            'CAMERA_WIDTH': 640,
            'CAMERA_HEIGHT': 480,
            'MIN_DETECTION_CONFIDENCE': 0.7,
            'MIN_TRACKING_CONFIDENCE': 0.5
        }
        
        for key, value in defaults.items():
            if key in self.config_vars:
                self.config_vars[key].set(value)
                
        messagebox.showinfo("Defaults Loaded", "Default configuration values have been loaded.")
        
    def save_config(self):
        """Save current configuration to file"""
        try:
            # Read current config file
            with open('config.py', 'r') as f:
                lines = f.readlines()
            
            # Update configuration values
            new_lines = []
            for line in lines:
                updated = False
                for key, var in self.config_vars.items():
                    if line.strip().startswith(f"{key} ="):
                        new_lines.append(f"{key} = {var.get()}\n")
                        updated = True
                        break
                if not updated:
                    new_lines.append(line)
            
            # Write updated config file
            with open('config.py', 'w') as f:
                f.writelines(new_lines)
                
            # Also save as JSON for backup
            config_dict = {key: var.get() for key, var in self.config_vars.items()}
            with open('gesture_config_backup.json', 'w') as f:
                json.dump(config_dict, f, indent=2)
                
            messagebox.showinfo("Configuration Saved", 
                              "Configuration has been saved successfully!\n"
                              "Restart the application to apply changes.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
            
    def test_config(self):
        """Test current configuration"""
        messagebox.showinfo("Test Configuration", 
                          "Configuration testing will launch the gesture test tool.\n"
                          "Use the test tool to verify your settings work correctly.")
        try:
            import subprocess
            subprocess.Popen(['python', 'test_gestures.py'], shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch test tool: {e}")
            
    def close_application(self):
        """Close the configuration GUI"""
        self.root.quit()
        self.root.destroy()
        
    def run(self):
        """Run the configuration GUI"""
        self.root.mainloop()

def main():
    """Main function for configuration GUI"""
    app = GestureConfigGUI()
    app.run()

if __name__ == "__main__":
    main()
