# habits endpoints

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, database
from app.crud import habits

router = APIRouter()

# create habit
@router.post("/habits", response_model=schemas.HabitResponse)
def create_habit(habit: schemas.HabitCreate, db: Session = Depends(database.get_db)):
    return habits.create_habit(db, habit)

# read all habits by user
@router.get("/habits", response_model=List[schemas.HabitResponse])
def read_habits(user_id: int, db: Session = Depends(database.get_db)):
    return habits.get_habits(db, user_id)

# read single habit
@router.get("/habits/{habit_id}", response_model=schemas.HabitResponse)
def read_habit(habit_id: int, user_id: int, db: Session = Depends(database.get_db)):
    db_habit = habits.get_habit(db, habit_id, user_id)
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return db_habit
    
# update habit
@router.put("/habits/{habit_id}", response_model=schemas.HabitResponse)
def update_habit(habit_id: int, habit: schemas.HabitUpdate, user_id: int, db: Session = Depends(database.get_db)):
    db_habit = habits.update_habit(db, habit_id, habit, user_id)
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return db_habit
    
# delete habit
@router.delete("/habits/{habit_id}", response_model=schemas.HabitResponse)
def delete_habit(habit_id: int, user_id: int, db: Session = Depends(database.get_db)):
    db_habit = habits.delete_habit(db, habit_id, user_id)
    if not db_habit: 
        raise HTTPException(status_code=404, detail="Habit not found")
    return db_habit