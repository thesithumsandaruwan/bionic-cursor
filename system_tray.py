"""
System Tray functionality for Hand Gesture Control
Provides background operation with system tray icon and controls
"""

import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox
import pystray
from pystray import MenuItem, Menu
from PIL import Image, ImageDraw

class SystemTray:
    def __init__(self, main_app_callback, quit_callback):
        """
        Initialize system tray
        
        Args:
            main_app_callback: Function to call the main application
            quit_callback: Function to call when quitting
        """
        self.main_app_callback = main_app_callback
        self.quit_callback = quit_callback
        self.icon = None
        self.is_running = False
        
    def create_icon_image(self, color='blue'):
        """Create a simple icon image"""
        # Create a simple hand icon
        image = Image.new('RGB', (64, 64), color='white')
        draw = ImageDraw.Draw(image)
        
        # Draw a simple hand shape
        # Palm
        draw.ellipse([20, 30, 44, 54], fill=color)
        
        # Fingers
        finger_positions = [
            (22, 15, 26, 35),  # thumb
            (28, 10, 32, 35),  # index
            (34, 8, 38, 35),   # middle
            (40, 12, 44, 35),  # ring
            (46, 18, 50, 35)   # pinky
        ]
        
        for pos in finger_positions:
            draw.rectangle(pos, fill=color)
            
        return image
    
    def show_about(self):
        """Show about dialog"""
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        messagebox.showinfo(
            "About Hand Gesture Control",
            "Hand Gesture Control v1.0\n\n"
            "Control your mouse using hand gestures!\n\n"
            "Gestures:\n"
            "• Open palm: Idle\n"
            "• Move hand: Move cursor\n"
            "• Thumb + Index pinch: Left click\n"
            "• Hold pinch + move: Drag\n"
            "• Index + Middle touch: Right click\n"
            "• Pinky up + move: Scroll\n\n"
            "Right-click tray icon for options."
        )
        root.destroy()
    
    def show_help(self):
        """Show help dialog"""
        root = tk.Tk()
        root.withdraw()
        
        messagebox.showinfo(
            "Hand Gesture Control - Help",
            "USAGE:\n"
            "1. Make sure your camera is connected\n"
            "2. Position your hand in front of the camera\n"
            "3. Use gestures to control your mouse\n\n"
            "GESTURES:\n"
            "• IDLE: Open palm (all fingers extended)\n"
            "• MOVE: Move your whole hand to move cursor\n"
            "• LEFT CLICK: Quick thumb + index finger pinch\n"
            "• DRAG: Hold thumb + index pinch while moving\n"
            "• RIGHT CLICK: Touch index + middle finger together\n"
            "• SCROLL: Only pinky finger up, move up/down\n\n"
            "TIPS:\n"
            "• Keep hand 1-2 feet from camera\n"
            "• Ensure good lighting\n"
            "• Move slowly and deliberately\n"
            "• Practice gestures for better recognition"
        )
        root.destroy()
    
    def open_normal_mode(self):
        """Start application in normal mode (with camera window)"""
        threading.Thread(target=lambda: self.main_app_callback(headless=False, silent=False), daemon=True).start()
    
    def restart_headless(self):
        """Restart application in headless mode"""
        threading.Thread(target=lambda: self.main_app_callback(headless=True, silent=False), daemon=True).start()
    
    def quit_application(self):
        """Quit the application"""
        self.is_running = False
        if self.icon:
            self.icon.stop()
        if self.quit_callback:
            self.quit_callback()
    
    def create_menu(self):
        """Create the system tray menu"""
        return Menu(
            MenuItem("Hand Gesture Control", self.show_about, default=True),
            Menu.SEPARATOR,
            MenuItem("Open Camera Window", self.open_normal_mode),
            MenuItem("Restart Headless", self.restart_headless),
            Menu.SEPARATOR,
            MenuItem("Help", self.show_help),
            MenuItem("About", self.show_about),
            Menu.SEPARATOR,
            MenuItem("Quit", self.quit_application)
        )
    
    def run(self):
        """Run the system tray"""
        try:
            # Create icon image
            icon_image = self.create_icon_image()
            
            # Create the system tray icon
            self.icon = pystray.Icon(
                "HandGestureControl",
                icon_image,
                "Hand Gesture Control",
                self.create_menu()
            )
            
            self.is_running = True
            
            # Run the icon (this blocks)
            self.icon.run()
            
        except Exception as e:
            print(f"System tray error: {e}")
            # Fallback: just run without system tray
            self.is_running = True
            try:
                while self.is_running:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass

def create_system_tray(main_app_callback, quit_callback):
    """
    Create and return a system tray instance
    
    Args:
        main_app_callback: Function to call the main application
        quit_callback: Function to call when quitting
        
    Returns:
        SystemTray instance
    """
    return SystemTray(main_app_callback, quit_callback)
