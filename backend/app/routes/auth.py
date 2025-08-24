# registry and authenticate

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import models, schemas, database
from app.utils import hash_password

router = APIRouter()


@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = (
        db.query(models.User)
        .filter(
            or_(models.User.username == user.username, models.User.email == user.email)
        )
        .first()
    )
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username or email already registered"
        )

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),  # later we change it to hashed
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ----- Current user dependency -----
def get_current_user(
    user_id: int = Header(
        ..., description="ID of the user"
    ),  # transffered into header X-User-Id
    db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user
