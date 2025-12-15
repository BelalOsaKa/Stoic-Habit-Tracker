# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Stoic Habit Tracker
Run: pyinstaller build_exe.spec
"""

import sys
from pathlib import Path

block_cipher = None

# Get the project root directory
project_root = Path(SPECPATH)

# Application metadata
app_name = "StoicHabitTracker"
app_icon = project_root / "Gemini_Generated_Image_vhbkywvhbkywvhbk.ico"

# Data files to include
datas = [
    (str(app_icon), "."),  # Include icon in root of dist folder
]

# Hidden imports (modules that PyInstaller might miss)
hiddenimports = [
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',
    'sqlalchemy',
    'sqlalchemy.orm',
    'sqlalchemy.engine',
    'sqlalchemy.pool',
    'sqlalchemy.sql',
    'matplotlib',
    'matplotlib.backends.backend_qtagg',
    'matplotlib.figure',
    'pandas',
    'numpy',
    'dateutil',
    'dateutil.parser',
    'dateutil.relativedelta',
    'plyer',
    'xml',
    'xml.parsers',
    'xml.parsers.expat',
    'plistlib',
    'pkg_resources',
    'ui.main_window',
    'ui.pages.dashboard_page',
    'ui.pages.heatmap_page',
    'ui.pages.charts_page',
    'ui.pages.settings_page',
    'ui.pages.widgets.category_combo',
    'ui.pages.widgets.habit_table',
    'db',
    'models',
    'controllers',
]

# Analysis
a = Analysis(
    [str(project_root / 'main.py')],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'unittest',
        'pydoc',
        'test',
        'tests',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# PyInstaller archive
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (GUI app)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(app_icon) if app_icon.exists() else None,
)

