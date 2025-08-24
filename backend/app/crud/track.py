from sqlalchemy.orm import Session
from app.models import HabitTrack, Habit
from app.schemas import TrackCreate


def create_track(db: Session, track: TrackCreate, user_id: int):
    # check that habit is exist
    db_habit = (
        db.query(Habit)
        .filter(Habit.id == track.habit_id, Habit.user_id == user_id)
        .first()
    )
    if not db_habit:
        return None

    db_track = HabitTrack(habit_id=track.habit_id, user_id=user_id)
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track


def get_tracks(db: Session, user_id: int, habit_id: int | None = None):
    query = db.query(HabitTrack).filter(HabitTrack.user_id == user_id)
    if habit_id:
        query = query.filter(HabitTrack.habit_id == habit_id)
    return query.all()


def delete_track(db: Session, track_id: int, user_id: int):
    db_track = (
        db.query(HabitTrack)
        .filter(HabitTrack.id == track_id, HabitTrack.user_id == user_id)
        .first()
    )
    if not db_track:
        return None
    db.delete(db_track)
    db.commit()
    return db_track
