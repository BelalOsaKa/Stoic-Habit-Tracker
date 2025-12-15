"""
Post-install script that runs automatically after MSI installation.
This creates shortcuts for the application.
"""
import os
import sys
import subprocess

def create_shortcuts_vbs(exe_path, icon_path):
    """Create shortcuts using VBScript (works without pywin32)"""
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    start_menu = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs")
    
    # Create Start Menu folder
    app_folder = os.path.join(start_menu, "Stoic Habit Tracker")
    os.makedirs(app_folder, exist_ok=True)
    
    desktop_shortcut = os.path.join(desktop, "Stoic Habit Tracker.lnk")
    start_menu_shortcut = os.path.join(app_folder, "Stoic Habit Tracker.lnk")
    
    # VBScript to create desktop shortcut
    vbs_desktop = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{desktop_shortcut}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{exe_path}"
oLink.WorkingDirectory = "{os.path.dirname(exe_path)}"
oLink.IconLocation = "{icon_path}"
oLink.Description = "Stoic Habit Tracker"
oLink.Save
'''
    
    # VBScript to create Start Menu shortcut
    vbs_start = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{start_menu_shortcut}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{exe_path}"
oLink.WorkingDirectory = "{os.path.dirname(exe_path)}"
oLink.IconLocation = "{icon_path}"
oLink.Description = "Stoic Habit Tracker"
oLink.Save
'''
    
    # Write and execute VBS scripts
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.vbs', delete=False) as f:
        f.write(vbs_desktop)
        vbs_file_desktop = f.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.vbs', delete=False) as f:
        f.write(vbs_start)
        vbs_file_start = f.name
    
    try:
        # Run VBS scripts silently
        subprocess.run(['cscript', '//nologo', vbs_file_desktop], check=False, capture_output=True)
        subprocess.run(['cscript', '//nologo', vbs_file_start], check=False, capture_output=True)
        return True
    except Exception as e:
        print(f"Error creating shortcuts: {e}")
        return False
    finally:
        # Clean up temp files
        try:
            os.remove(vbs_file_desktop)
            os.remove(vbs_file_start)
        except:
            pass

def main():
    """Main post-install function"""
    # Get installation directory from command line argument or environment
    if len(sys.argv) > 1:
        install_dir = sys.argv[1]
    else:
        # Try to get from common locations
        possible_locations = [
            r"C:\Program Files\Stoic Habit Tracker",
            r"C:\Program Files (x86)\Stoic Habit Tracker",
            os.path.join(os.path.expanduser("~"), "AppData", "Local", "Programs", "Stoic Habit Tracker"),
        ]
        install_dir = None
        for loc in possible_locations:
            if os.path.exists(os.path.join(loc, "StoicHabitTracker.exe")):
                install_dir = loc
                break
    
    if not install_dir:
        return 1
    
    exe_path = os.path.join(install_dir, "StoicHabitTracker.exe")
    icon_path = os.path.join(install_dir, "Gemini_Generated_Image_vhbkywvhbkywvhbk.ico")
    
    if not os.path.exists(exe_path):
        return 1
    
    # Create shortcuts
    if create_shortcuts_vbs(exe_path, icon_path):
        return 0
    return 1

if __name__ == "__main__":
    sys.exit(main())

