# PySide6 Monthly Habit Tracker


A modern desktop habit tracker built with PySide6, SQLite (SQLAlchemy), and Matplotlib.


Features:
- Add / edit / delete habits
- Categories for habits
- Checkboxes per day for the selected month
- Month navigation (previous / next month)
- Heatmap visualization (GitHub-style)
- Progress charts (Matplotlib embedded)
- Dark / Light theme
- Export to CSV
- Optional desktop notifications (using plyer)


## Run locally


1. Create and activate a virtualenv


```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows
venv\Scripts\activate