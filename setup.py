import sys
from cx_Freeze import setup, Executable
import os

# Application metadata
APP_NAME = "Stoic Habit Tracker"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "A modern desktop habit tracker built with PySide6"
APP_AUTHOR = "Your Name"
APP_ICON = "Gemini_Generated_Image_vhbkywvhbkywvhbk.ico"

# Build options
build_exe_options = {
    "packages": [
        "PySide6",
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
        "sqlalchemy",
        "sqlalchemy.orm",
        "sqlalchemy.engine",
        "matplotlib",
        "matplotlib.backends",
        "matplotlib.backends.backend_qtagg",
        "matplotlib.figure",
        "pandas",
        "numpy",
        "plyer",
        "dateutil",
        "urllib",
        "urllib.parse",
        "pathlib",
        "calendar",
        "datetime",
        "os",
        "sys"
    ],
    "includes": [
        "ui.main_window",
        "ui.pages.dashboard_page",
        "ui.pages.heatmap_page",
        "ui.pages.charts_page",
        "ui.pages.settings_page",
        "ui.pages.widgets.category_combo",
        "ui.pages.widgets.habit_table",
        "db",
        "models",
        "controllers"
    ],
    "include_files": [
        ("Gemini_Generated_Image_vhbkywvhbkywvhbk.ico", "Gemini_Generated_Image_vhbkywvhbkywvhbk.ico"),
        ("post_install.py", "post_install.py"),
    ],
    "excludes": [
        "tkinter",
        "unittest",
        "email",
        "http",
        "xml",
        "pydoc"
    ],
    "optimize": 2,
}

# MSI options
bdist_msi_options = {
    "upgrade_code": "{12345678-1234-1234-1234-123456789012}",
    "add_to_path": False,
    "initial_target_dir": r"[ProgramFilesFolder]\%s" % APP_NAME,
    "install_icon": APP_ICON,
    "all_users": False,  # Install for current user only (easier to find)
}

# Executable
executable = Executable(
    script="main.py",
    base="Win32GUI" if sys.platform == "win32" else None,
    icon=APP_ICON,
    target_name=APP_NAME.replace(" ", "") + ".exe"
)

setup(
    name=APP_NAME,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    author=APP_AUTHOR,
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options
    },
    executables=[executable]
)

