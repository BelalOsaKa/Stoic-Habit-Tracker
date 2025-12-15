"""
Simple script to create shortcuts for Stoic Habit Tracker.
Run this script after installation to create Start Menu and Desktop shortcuts.
"""
import os
import sys

try:
    import win32com.client
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False
    print("Warning: pywin32 not available. Using alternative method.")

def create_shortcut_win32(target_path, shortcut_path, icon_path=None, description=""):
    """Create a Windows shortcut using win32com"""
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target_path
    shortcut.WorkingDirectory = os.path.dirname(target_path)
    if icon_path and os.path.exists(icon_path):
        shortcut.IconLocation = icon_path
    if description:
        shortcut.Description = description
    shortcut.save()
    return True

def create_shortcut_vbs(target_path, shortcut_path, icon_path=None):
    """Create shortcut using VBScript (fallback method)"""
    vbs_script = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{target_path}"
oLink.WorkingDirectory = "{os.path.dirname(target_path)}"
'''
    if icon_path and os.path.exists(icon_path):
        vbs_script += f'oLink.IconLocation = "{icon_path}"\n'
    vbs_script += 'oLink.Save\n'
    
    vbs_file = os.path.join(os.path.dirname(shortcut_path), "create_shortcut_temp.vbs")
    try:
        with open(vbs_file, 'w') as f:
            f.write(vbs_script)
        os.system(f'cscript //nologo "{vbs_file}"')
        os.remove(vbs_file)
        return True
    except Exception as e:
        print(f"Error creating shortcut with VBScript: {e}")
        return False

def main():
    """Create shortcuts for the application"""
    # Possible installation locations
    possible_locations = [
        r"C:\Program Files\Stoic Habit Tracker",
        r"C:\Program Files (x86)\Stoic Habit Tracker",
        os.path.join(os.path.expanduser("~"), "AppData", "Local", "Programs", "Stoic Habit Tracker"),
    ]
    
    exe_path = None
    icon_path = None
    
    # Find the installation
    for location in possible_locations:
        test_exe = os.path.join(location, "StoicHabitTracker.exe")
        if os.path.exists(test_exe):
            exe_path = test_exe
            icon_path = os.path.join(location, "Gemini_Generated_Image_vhbkywvhbkywvhbk.ico")
            print(f"Found installation at: {location}")
            break
    
    if not exe_path:
        print("Error: Could not find Stoic Habit Tracker installation.")
        print("Please run this script from the installation directory or specify the path.")
        print("\nTried locations:")
        for loc in possible_locations:
            print(f"  - {loc}")
        return 1
    
    # Get user directories
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    start_menu = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs")
    
    # Create Start Menu folder
    app_folder = os.path.join(start_menu, "Stoic Habit Tracker")
    os.makedirs(app_folder, exist_ok=True)
    
    # Create shortcuts
    desktop_shortcut = os.path.join(desktop, "Stoic Habit Tracker.lnk")
    start_menu_shortcut = os.path.join(app_folder, "Stoic Habit Tracker.lnk")
    
    success = False
    if HAS_WIN32:
        try:
            create_shortcut_win32(exe_path, desktop_shortcut, icon_path, "Stoic Habit Tracker")
            create_shortcut_win32(exe_path, start_menu_shortcut, icon_path, "Stoic Habit Tracker")
            success = True
        except Exception as e:
            print(f"Error with win32 method: {e}")
    
    if not success:
        print("Trying alternative method...")
        if create_shortcut_vbs(exe_path, desktop_shortcut, icon_path):
            create_shortcut_vbs(exe_path, start_menu_shortcut, icon_path)
            success = True
    
    if success:
        print(f"\n✓ Created desktop shortcut: {desktop_shortcut}")
        print(f"✓ Created Start Menu shortcut: {start_menu_shortcut}")
        print("\nShortcuts created successfully!")
        return 0
    else:
        print("\nFailed to create shortcuts. You can create them manually:")
        print(f"1. Right-click on: {exe_path}")
        print("2. Select 'Send to' > 'Desktop (create shortcut)'")
        return 1

if __name__ == "__main__":
    sys.exit(main())

