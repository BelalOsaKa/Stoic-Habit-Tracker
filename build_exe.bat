@echo off
REM Build script for creating executable with PyInstaller
echo Building Stoic Habit Tracker executable...
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller is not installed. Installing...
    pip install pyinstaller
    if errorlevel 1 (
        echo Failed to install PyInstaller. Please install it manually: pip install pyinstaller
        pause
        exit /b 1
    )
)

REM Clean previous builds
if exist "build" (
    echo Cleaning previous build...
    rmdir /s /q build
)
if exist "dist" (
    echo Cleaning previous dist...
    rmdir /s /q dist
)

REM Run PyInstaller
echo Running PyInstaller...
pyinstaller build_exe.spec

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo Executable location: dist\StoicHabitTracker.exe
echo.
pause

