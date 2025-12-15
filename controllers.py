from datetime import date
import calendar
from sqlalchemy import and_
# session creator
from db import get_session
#import ORM models
from models import Habit, HabitDay

def days_in_month(year:int, month:int) -> int:
    """
    Returns how many days exist in a given year/month.
    Example: days_in_month(2025,2) -> 28
    """
    return calendar.monthrange(year,month)[1]

def ensure_month_entries(year:int, month:int):
    session =get_session()

    try:
        habits = session.query(Habit).all()

        for habit in habits:
            for day in range (1, days_in_month(year, month) + 1):
                d = date(year, month, day)
                existing = session.query(HabitDay).filter_by(
                    habit_id=habit.id,
                    date=d
                ).first()
                if not existing:
                    session.add(HabitDay(
                        habit_id=habit.id,
                        date=d,
                        checked=False
                    )
                    )
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_month_table(year:int, month:int):
    session = get_session()
    try:
        ensure_month_entries(year, month)
        habits = session.query(Habit).order_by(Habit.id).all()
        table = []
        for habit in habits:
            days_rows = session.query(HabitDay).filter(
                and_(
                    HabitDay.habit_id == habit.id,
                    HabitDay.date >= date(year, month, 1),
                    HabitDay.date <= date(year, month, days_in_month(year, month))
                )
            ).order_by(HabitDay.date).all()
            table.append((habit,days_rows))
        return table

    finally:
        session.close()

def toggle_habit_day(habit_day_id:int):
    session = get_session()
    try:
        habit_day = session.query(HabitDay).get(habit_day_id)
        habit_day.checked = not habit_day.checked
        session.commit()
        return habit_day
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def add_habit(name:str, category:str=None):
    session = get_session()
    try:
        habit = Habit(name=name, category=category)
        session.add(habit)
        session.commit()
        return habit
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        
def edit_habit(habit_id:int, name:str, category:str=None):
    session = get_session()
    try:
        habit = session.query(Habit).get(habit_id)
        if  name:
            habit.name = name
        if category:
            habit.category = category
        session.commit()
        return habit
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def delete_habit(habit_id:int):
    session = get_session()
    try:
        habit = session.query(Habit).get(habit_id)
        session.delete(habit)
        session.commit()

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def export_month_csv(year: int, month: int, filename: str):
    """
    Write the habit tracking data for the selected month to a CSV file.
    """
    import csv

    session = get_session()

    try:
        table = get_month_table(year, month)
        days = days_in_month(year, month)

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # CSV header
            header = ["Habit"] + [str(d) for d in range(1, days + 1)] + ["%"]
            writer.writerow(header)

            # CSV rows
            for habit, rows in table:
                checked_count = sum(1 for r in rows if r.checked)
                percent = round(checked_count / days * 100, 1)

                row = (
                    [habit.name] +
                    [(1 if r.checked else 0) for r in rows] +
                    [percent]
                )

                writer.writerow(row)

    finally:
        session.close()

def get_all_habits_full():
    """
    Returns all habits with all their HabitDay entries across all months.
    Returns: list of (habit, [HabitDay]) tuples
    """
    session = get_session()
    try:
        habits = session.query(Habit).order_by(Habit.id).all()
        result = []
        for habit in habits:
            days_rows = session.query(HabitDay).filter(
                HabitDay.habit_id == habit.id
            ).order_by(HabitDay.date).all()
            result.append((habit, days_rows))
        return result
    finally:
        session.close()

def clear_all_data():
    """
    Deletes all habits and habit days from the database.
    """
    session = get_session()
    try:
        # Delete all habit days first (foreign key constraint)
        session.query(HabitDay).delete()
        # Then delete all habits
        session.query(Habit).delete()
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def calculate_streak(day_rows):
    """
    Receives a list of HabitDay objects for one month.
    Returns (current_streak, longest_streak).
    """

    longest = 0
    current = 0

    for day in day_rows:
        if day.checked:
            current += 1
            longest = max(longest, current)
        else:
            current = 0

    return current, longest
def get_weekly_summary(year, month):
    """
    Returns dict:
    {
        'total': int,
        'best_day': int,
        'worst_day': int,
        'percent': float
    }
    """

    table = get_month_table(year, month)
    summary = [0] * 31  # max days in any month

    for habit, day_rows in table:
        for i, d in enumerate(day_rows):
            if d.checked:
                summary[i] += 1

    # Remove unused padding
    summary = summary[:days_in_month(year, month)]

    total = sum(summary)
    best = summary.index(max(summary)) + 1
    worst = summary.index(min(summary)) + 1
    percent = round((total / (len(table) * len(summary))) * 100, 1) if table else 0

    return {
        "total": total,
        "best_day": best,
        "worst_day": worst,
        "percent": percent
    }

