# PowerShell build script for creating executable with PyInstaller
Write-Host "Building Stoic Habit Tracker executable..." -ForegroundColor Green
Write-Host ""

# Check if PyInstaller is installed
try {
    python -c "import PyInstaller" 2>$null
    if ($LASTEXITCODE -ne 0) { throw }
} catch {
    Write-Host "PyInstaller is not installed. Installing..." -ForegroundColor Yellow
    pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install PyInstaller. Please install it manually: pip install pyinstaller" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Clean previous builds
if (Test-Path "build") {
    Write-Host "Cleaning previous build..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "build"
}
if (Test-Path "dist") {
    Write-Host "Cleaning previous dist..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "dist"
}

# Run PyInstaller
Write-Host "Running PyInstaller..." -ForegroundColor Green
pyinstaller build_exe.spec

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Build completed successfully!" -ForegroundColor Green
Write-Host "Executable location: dist\StoicHabitTracker.exe" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to exit"

