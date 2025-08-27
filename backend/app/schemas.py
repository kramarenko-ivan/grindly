# Pydantic schemas

from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

from datetime import datetime


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


# ---------- Auth ----------
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: str | None = None


# ---------- Habit ----------
class HabitBase(BaseModel):
    title: str
    description: Optional[str] = None


class HabitCreate(BaseModel):
    title: str
    description: Optional[str] = None
    user_id: int


class HabitUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class HabitResponse(HabitBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


# ---------- Track ----------
class TrackCreate(BaseModel):
    habit_id: int


class TrackResponse(BaseModel):
    id: int
    habit_id: int
    user_id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
