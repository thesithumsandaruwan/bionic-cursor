# Build script for creating Windows installer
import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    print(f"Running: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print("✓ Success")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False

def check_requirements():
    """Check if required tools are installed"""
    print("Checking requirements...")
    
    # Check Python
    try:
        import sys
        print(f"✓ Python {sys.version}")
    except:
        print("✗ Python not found")
        return False
    
    # Check PyInstaller
    try:
        import PyInstaller
        print(f"✓ PyInstaller found")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        if not run_command("pip install pyinstaller", "Installing PyInstaller"):
            return False
    
    return True

def build_executable():
    """Build the executable using PyInstaller"""
    print("\n" + "="*50)
    print("BUILDING EXECUTABLE")
    print("="*50)
    
    # Change to parent directory
    os.chdir('..')
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--add-data", "config.py;.",
        "--add-data", "system_tray.py;.",
        "--add-data", "selected_camera.txt;.",
        "--hidden-import", "cv2",
        "--hidden-import", "mediapipe",
        "--hidden-import", "pynput",
        "--hidden-import", "pystray",
        "--hidden-import", "PIL",
        "--hidden-import", "tkinter",
        "--icon", "installer/icon.ico",
        "--name", "HandGestureControl",
        "main.py"
    ]
    
    cmd_str = " ".join(cmd)
    return run_command(cmd_str, "Building executable with PyInstaller")

def create_installer_files():
    """Create additional installer files"""
    print("\n" + "="*50)
    print("CREATING INSTALLER FILES")
    print("="*50)
    
    # Create installer directory structure
    installer_dir = Path("installer")
    installer_dir.mkdir(exist_ok=True)
    
    # Copy built executable
    dist_dir = Path("dist")
    if dist_dir.exists() and (dist_dir / "HandGestureControl.exe").exists():
        shutil.copy2(dist_dir / "HandGestureControl.exe", installer_dir / "HandGestureControl.exe")
        print("✓ Copied executable to installer directory")
    else:
        print("✗ Executable not found in dist directory")
        return False
    
    # Copy documentation
    docs_to_copy = ["README.md", "LATEST_UPDATES.md", "requirements.txt"]
    for doc in docs_to_copy:
        if Path(doc).exists():
            shutil.copy2(doc, installer_dir / doc)
            print(f"✓ Copied {doc}")
    
    return True

def main():
    """Main build process"""
    print("Hand Gesture Control - Windows Installer Builder")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n✗ Requirements check failed. Please install missing components.")
        return False
    
    # Build executable
    if not build_executable():
        print("\n✗ Failed to build executable")
        return False
    
    # Create installer files
    if not create_installer_files():
        print("\n✗ Failed to create installer files")
        return False
    
    print("\n" + "="*50)
    print("BUILD COMPLETE!")
    print("="*50)
    print("Files created in 'installer' directory:")
    print("- HandGestureControl.exe (main executable)")
    print("- Documentation files")
    print("\nNext steps:")
    print("1. Run 'create_installer.iss' with Inno Setup to create the installer")
    print("2. Or use the batch files for easy installation")
    
    return True

if __name__ == "__main__":
    main()
