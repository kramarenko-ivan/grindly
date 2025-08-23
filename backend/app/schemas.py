# Pydantic schemas 

from pydantic import BaseModel, ConfigDict, EmailStr
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

    model_config = ConfigDict(from_attributes=True)

# ---------- Habit ----------
class HabitBase(BaseModel):
    title: str
    description: Optional[str] = None

class HabitCreate(BaseModel):
    pass

class HabitUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class HabitResponse(HabitBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)