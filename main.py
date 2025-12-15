import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

# Database setup
from db import init_db
from models import Base

# Main UI Window
from ui.main_window import MainWindow

def get_icon_path():
    """Get the path to the icon file, works both as script and executable."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        # In onefile mode, resources are extracted to sys._MEIPASS
        if hasattr(sys, '_MEIPASS'):
            base_path = Path(sys._MEIPASS)
        else:
            # In onedir mode, resources are next to the executable
            base_path = Path(sys.executable).parent
    else:
        # Running as script
        base_path = Path(__file__).parent
    
    icon_path = base_path / "Gemini_Generated_Image_vhbkywvhbkywvhbk.ico"
    return str(icon_path) if icon_path.exists() else None

class AppController:
    """
    Holds the currently selected month and year.
    Also provides helper functions to move between months.
    """

    def __init__(self):
        from datetime import datetime

        #get current month/year

        today = datetime.today()
        self.year = today.year
        self.month = today.month

    def next_month(self):
        #Move to the next calendar month.

        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1

    def prev_month(self):
        #Move to the previous calendar month.

        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1

#app startup

def main():
    #Main function — starts the Qt application.

    #initialize (or create) the database
    init_db(Base)

    #create Qt app
    app = QApplication(sys.argv)
    
    # Set application icon
    icon_path = get_icon_path()
    if icon_path:
        app.setWindowIcon(QIcon(icon_path))

    #create the controller for month / year
    controller = AppController()

    #create the main window
    window = MainWindow(controller)
    window.show()

    #start Qt event loop 
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

#1078 line of code