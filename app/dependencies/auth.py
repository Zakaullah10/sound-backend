from fastapi import Depends, HTTPException,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from jose import jwt , JWTError
from sqlalchemy.orm import Session
import os

from app.core.database import get_db
from app.models.user import User

security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


def get_current_user(
        credentials:HTTPAuthorizationCredentials = Depends(security),
        db:Session=Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None :
            raise HTTPException(
                status_code=401,
                detail="Invaild token"
            )

    except JWTError:
        raise HTTPException(
             status_code=401,
             detail="Invalid or expired token"
        )

    user =db.query(User).filter(User.id == int(user_id)).first()

    if user  is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    
    return user


def get_current_admin(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user