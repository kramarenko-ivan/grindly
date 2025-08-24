# SQLAlchemy models

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime, timezone
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    # connect with habits
    habits = relationship("Habit", back_populates="user")


class Habit(Base):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # connect with user
    user = relationship("User", back_populates="habits")

    tracks = relationship(
        "HabitTrack", back_populates="habit", cascade="all, delete-orphan"
    )


class HabitTrack(Base):
    __tablename__ = "habit_tracks"
    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    habit = relationship("Habit", back_populates="tracks")
    user = relationship("User")
