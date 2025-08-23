from sqlalchemy.orm import Session
from app.models import Habit, User
from app.schemas import HabitCreate, HabitUpdate

def create_habit(db: Session, habit: HabitCreate):
    # check for user existing
    user = db.query(User).filter(User.id == habit.user_id).first()
    if not user:
        return None
    db_habit = Habit(**habit.model_dump())
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

def get_habits(db: Session, user_id: int):
    return db.query(Habit).filter(Habit.user_id == user_id).all()

def get_habit(db: Session, habit_id: int, user_id: int):
    return db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == user_id).first()

def update_habit(db: Session, habit_id: int, habit: HabitUpdate):
    db_habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not db_habit:
        return None
    for key, value in habit.model_dump(exclude_unset=True).items():
        setattr(db_habit, key, value)
    db.commit()
    db.refresh(db_habit)
    return db_habit

def delete_habit(db: Session, habit_id: int):
    db_habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not db_habit:
        return None
    db.delete(db_habit)
    db.commit()
    return db_habit