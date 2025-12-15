"""
Post-install script to create shortcuts for the application.
This script is run after MSI installation to create Start Menu and Desktop shortcuts.
"""
import os
import sys
import win32com.client

def create_shortcut(target_path, shortcut_path, icon_path=None, description=""):
    """Create a Windows shortcut (.lnk file)"""
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target_path
    shortcut.WorkingDirectory = os.path.dirname(target_path)
    if icon_path:
        shortcut.IconLocation = icon_path
    if description:
        shortcut.Description = description
    shortcut.save()

def main():
    """Create shortcuts after installation"""
    # Get installation directory from environment or use default
    install_dir = os.environ.get('INSTALLDIR', r'C:\Program Files\Stoic Habit Tracker')
    exe_path = os.path.join(install_dir, 'StoicHabitTracker.exe')
    icon_path = os.path.join(install_dir, 'Gemini_Generated_Image_vhbkywvhbkywvhbk.ico')
    
    if not os.path.exists(exe_path):
        print(f"Error: Executable not found at {exe_path}")
        return 1
    
    # Get user directories
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    start_menu = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs")
    
    # Create Start Menu folder
    app_folder = os.path.join(start_menu, "Stoic Habit Tracker")
    os.makedirs(app_folder, exist_ok=True)
    
    # Create shortcuts
    try:
        # Desktop shortcut
        desktop_shortcut = os.path.join(desktop, "Stoic Habit Tracker.lnk")
        create_shortcut(exe_path, desktop_shortcut, icon_path, "Stoic Habit Tracker")
        print(f"Created desktop shortcut: {desktop_shortcut}")
        
        # Start Menu shortcut
        start_menu_shortcut = os.path.join(app_folder, "Stoic Habit Tracker.lnk")
        create_shortcut(exe_path, start_menu_shortcut, icon_path, "Stoic Habit Tracker")
        print(f"Created Start Menu shortcut: {start_menu_shortcut}")
        
        return 0
    except Exception as e:
        print(f"Error creating shortcuts: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

