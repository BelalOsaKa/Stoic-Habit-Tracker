# Building the Executable

This guide explains how to build the Stoic Habit Tracker as a standalone Windows executable.

## Prerequisites

1. Python 3.9 or higher installed
2. All dependencies installed (run `pip install -r requirements.txt`)
3. PyInstaller installed (will be installed automatically by the build script)

## Quick Build

### Option 1: Using Batch Script (Windows)
Double-click `build_exe.bat` or run it from command prompt:
```batch
build_exe.bat
```

### Option 2: Using PowerShell Script
Right-click `build_exe.ps1` and select "Run with PowerShell" or run:
```powershell
.\build_exe.ps1
```

### Option 3: Manual Build
```bash
pip install pyinstaller
pyinstaller build_exe.spec
```

## Output

After building, you'll find the executable at:
```
dist\StoicHabitTracker.exe
```

## What Changed

- **Database Location**: The database (`tracker.sqlite`) will now be created in the same directory as the executable when running as a compiled app. This ensures the database persists and is accessible.

- **Single Executable**: PyInstaller creates a single executable file that includes all dependencies, so you don't need Python installed on the target machine.

## Distribution

To distribute your application:
1. Copy `dist\StoicHabitTracker.exe` to the target machine
2. The executable is standalone - no installation needed
3. The database will be created automatically in the same folder as the executable

## Troubleshooting

### Build Fails
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Make sure PyInstaller is installed: `pip install pyinstaller`
- Check that the icon file exists: `Gemini_Generated_Image_vhbkywvhbkywvhbk.ico`

### Executable Doesn't Run
- Try running from command line to see error messages
- Check Windows Defender or antivirus (sometimes flags new executables)
- Make sure all required DLLs are included (PyInstaller should handle this)

### Database Issues
- The database is created in the same folder as the executable
- Make sure the executable has write permissions in that folder
- If running from a read-only location, move the executable to a writable folder

## Notes

- The first build may take several minutes
- The executable will be large (100-200MB) because it includes all dependencies
- Subsequent builds are faster due to caching

