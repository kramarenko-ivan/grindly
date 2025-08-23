# Pydantic schemas 

from pydantic import BaseModel, EmailStr
from typing import Optional

# ---------- User ----------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

# ---------- Habit ----------
class HabitBase(BaseModel):
    title: str
    desctiption: Optional[str] = None

class HabitCreate(BaseModel):
    pass

class HabitUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class HabitResponse(HabitBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True