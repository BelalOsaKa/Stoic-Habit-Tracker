# models.py
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey

#creat a base class for all models
Base = declarative_base()


class Habit(Base):
    __tablename__ = 'habits'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=True)

    days = relationship('HabitDay', back_populates='habit', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Habit id={self.id} name={self.name}>"


class HabitDay(Base):
    __tablename__ = 'habit_days'

    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey('habits.id'), nullable=False)
    date = Column(Date, nullable=False)
    checked = Column(Boolean, default=False)

    habit = relationship('Habit', back_populates='days')

    def __repr__(self):
        return f"<HabitDay id={self.id} habit_id={self.habit_id} date={self.date} checked={self.checked}>"