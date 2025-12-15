import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import date
import calendar

DB_NAME = "tracker.db"


# ---------------- DATABASE ---------------- #
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS habits(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS habit_days(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            day INTEGER NOT NULL,
            checked INTEGER DEFAULT 0,
            FOREIGN KEY (habit_id) REFERENCES habits(id)
        )
    """)

    conn.commit()
    conn.close()


def get_habits():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name FROM habits ORDER BY id")
    rows = c.fetchall()
    conn.close()
    return rows


def add_habit(name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO habits (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()


def delete_habit(habit_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    c.execute("DELETE FROM habit_days WHERE habit_id = ?", (habit_id,))
    conn.commit()
    conn.close()


def edit_habit(habit_id, new_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE habits SET name = ? WHERE id = ?", (new_name, habit_id))
    conn.commit()
    conn.close()


def ensure_month_days(habit_id, year, month):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    days = calendar.monthrange(year, month)[1]

    for d in range(1, days + 1):
        c.execute("""
            SELECT id FROM habit_days 
            WHERE habit_id=? AND year=? AND month=? AND day=?
        """, (habit_id, year, month, d))
        if not c.fetchone():
            c.execute("""
                INSERT INTO habit_days(habit_id, year, month, day, checked)
                VALUES (?, ?, ?, ?, 0)
            """, (habit_id, year, month, d))

    conn.commit()
    conn.close()


def toggle_day(habit_day_id, value):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        UPDATE habit_days SET checked=? WHERE id=?
    """, (1 if value else 0, habit_day_id))
    conn.commit()
    conn.close()


def get_month_data(year, month):
    """Returns: list of (habit_id, habit_name, [ (day, checked, habit_day_id),... ])"""

    habits = get_habits()
    month_data = []
    days = calendar.monthrange(year, month)[1]

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    for habit_id, name in habits:
        ensure_month_days(habit_id, year, month)

        c.execute("""
            SELECT id, day, checked 
            FROM habit_days
            WHERE habit_id=? AND year=? AND month=?
            ORDER BY day
        """, (habit_id, year, month))

        rows = c.fetchall()
        # rows = [(habit_day_id, day, checked), ...]
        formatted = [(r[1], r[2], r[0]) for r in rows]
        month_data.append((habit_id, name, formatted))

    conn.close()
    return month_data


# ---------------- UI CLASS ---------------- #
class HabitTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monthly Habit Tracker")

        self.year = date.today().year
        self.month = date.today().month

        self.create_ui()
        self.refresh()

    # -------- UI Layout -------- #
    def create_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        tk.Label(top_frame, text=f"Monthly Habit Tracker ({calendar.month_name[self.month]} {self.year})",
                 font=("Arial", 16, "bold")).pack()

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Habit", command=self.add_habit_dialog).grid(row=0, column=0, padx=5)

        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(pady=10)

    # -------- Table Refresh -------- #
    def refresh(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        month_data = get_month_data(self.year, self.month)
        days = calendar.monthrange(self.year, self.month)[1]

        # Header row
        tk.Label(self.table_frame, text="Habit", font=("Arial", 12, "bold"), width=18).grid(row=0, column=0)
        for d in range(1, days + 1):
            tk.Label(self.table_frame, text=str(d), width=3).grid(row=0, column=d)

        tk.Label(self.table_frame, text="%", font=("Arial", 12, "bold")).grid(row=0, column=days+1)
        tk.Label(self.table_frame, text="Actions", font=("Arial", 12, "bold")).grid(row=0, column=days+2)

        # Habit rows
        row = 1
        for habit_id, habit_name, records in month_data:
            tk.Label(self.table_frame, text=habit_name, width=18).grid(row=row, column=0)

            checked_count = 0
            for (day, checked, habit_day_id) in records:
                var = tk.IntVar(value=checked)
                cb = tk.Checkbutton(
                    self.table_frame,
                    variable=var,
                    command=lambda id=habit_day_id, v=var: self.toggle(id, v)
                )
                cb.grid(row=row, column=day)
                if checked:
                    checked_count += 1

            # % discipline
            percent = round((checked_count / days) * 100, 1)
            tk.Label(self.table_frame, text=f"{percent}%", width=6).grid(row=row, column=days+1)

            # Actions
            tk.Button(self.table_frame, text="Edit",
                      command=lambda hid=habit_id, old=habit_name: self.edit_habit_dialog(hid, old)).grid(row=row, column=days+2)
            tk.Button(self.table_frame, text="Delete",
                      command=lambda hid=habit_id: self.delete_habit_action(hid)).grid(row=row, column=days+3)

            row += 1

    # -------- Checkbox toggling -------- #
    def toggle(self, habit_day_id, var):
        toggle_day(habit_day_id, var.get())
        self.refresh()

    # -------- Habit management -------- #
    def add_habit_dialog(self):
        name = simpledialog.askstring("Add Habit", "Enter habit name:")
        if name:
            add_habit(name)
            self.refresh()

    def edit_habit_dialog(self, habit_id, old_name):
        new_name = simpledialog.askstring("Edit Habit", "New name:", initialvalue=old_name)
        if new_name:
            edit_habit(habit_id, new_name)
            self.refresh()

    def delete_habit_action(self, habit_id):
        if messagebox.askyesno("Confirm", "Delete this habit?"):
            delete_habit(habit_id)
            self.refresh()


# ---------------- RUN APP ---------------- #
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = HabitTrackerApp(root)
    root.mainloop()
