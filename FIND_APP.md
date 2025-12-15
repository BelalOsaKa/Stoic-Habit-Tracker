# Finding Your Installed Application

If you can't find the app after installation, try these locations:

## Common Installation Locations:

1. **Program Files (64-bit)**
   - `C:\Program Files\Stoic Habit Tracker\StoicHabitTracker.exe`

2. **Program Files (32-bit)**
   - `C:\Program Files (x86)\Stoic Habit Tracker\StoicHabitTracker.exe`

3. **User AppData**
   - `C:\Users\[YourUsername]\AppData\Local\Programs\Stoic Habit Tracker\StoicHabitTracker.exe`

## Quick Ways to Find It:

### Method 1: Search Windows
1. Press `Windows Key + S`
2. Type "Stoic Habit Tracker"
3. Look for the application in search results

### Method 2: Check Installed Programs
1. Open **Settings** > **Apps** > **Installed apps**
2. Search for "Stoic Habit Tracker"
3. Click on it and select "Open file location"

### Method 3: Use File Explorer
1. Open File Explorer
2. Navigate to `C:\Program Files\`
3. Look for "Stoic Habit Tracker" folder

## Creating Shortcuts:

After finding the app, you can:

1. **Run the shortcut creation script:**
   ```powershell
   python create_shortcuts_simple.py
   ```

2. **Or create shortcuts manually:**
   - Right-click on `StoicHabitTracker.exe`
   - Select "Send to" > "Desktop (create shortcut)"
   - For Start Menu: Copy the shortcut to:
     `C:\Users\[YourUsername]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs`

