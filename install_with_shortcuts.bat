@echo off
REM Automated installer that installs MSI and creates shortcuts
echo Installing Stoic Habit Tracker...
echo.

REM Find the MSI file
set MSI_FILE=dist\Stoic Habit Tracker-1.0.0-win64.msi

if not exist "%MSI_FILE%" (
    echo Error: MSI file not found at %MSI_FILE%
    echo Please build the MSI first using: python setup.py bdist_msi
    pause
    exit /b 1
)

REM Install the MSI
echo Installing MSI package...
msiexec /i "%MSI_FILE%" /qn /norestart
if errorlevel 1 (
    echo Installation failed!
    pause
    exit /b 1
)

echo.
echo Installation complete!
echo Creating shortcuts...

REM Wait a moment for installation to complete
timeout /t 2 /nobreak >nul

REM Run the post-install script to create shortcuts
python post_install.py

echo.
echo Done! Shortcuts have been created on your Desktop and Start Menu.
pause

