import os
from passlib.context import CryptContext
from jose import jwt
from typing import Optional, Dict, Any
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

# Creating context for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        os.getenv("SECRET_KEY", "defaultsecret"),
        algorithm=os.getenv("ALGORITHM", "HS256"),
    )
    return encoded_jwt
