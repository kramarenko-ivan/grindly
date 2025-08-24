from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app import schemas, database
from app.crud import track

router = APIRouter()


@router.post("/track", response_model=schemas.TrackResponse)
def create_track(
    track_schema: schemas.TrackCreate,
    user_id: int,
    db: Session = Depends(database.get_db),
):
    db_track = track.create_track(db, track_schema, user_id)
    if not db_track:
        raise HTTPException(status_code=404, detail="Habit not found for this user")
    return db_track


@router.get("/track", response_model=List[schemas.TrackResponse])
def read_tracks(
    user_id: int, habit_id: Optional[int] = None, db: Session = Depends(database.get_db)
):
    return track.get_tracks(db, user_id, habit_id)


@router.get("/track/{track_id}", response_model=schemas.TrackResponse)
def read_track(track_id: int, user_id: int, db: Session = Depends(database.get_db)):
    db_track = track.get_track(db, track_id, user_id)
    if not db_track:
        raise HTTPException(status_code=404, detail="Track not found")


@router.delete("/track/{track_id}")
def delete_track(track_id: int, user_id: int, db: Session = Depends(database.get_db)):
    db_track = track.delete_track(db, track_id=track_id, user_id=user_id)
    if not db_track:
        raise HTTPException(status_code=404, detail="Track not found")
    return {"detail": "Track deleted"}
