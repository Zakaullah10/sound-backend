from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.security import hash_password,verify_password,create_access_token,create_refresh_token
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserLogin
from jose import jwt , JWTError
import secrets
from datetime import  datetime , timedelta
import os


router = APIRouter(tags=["Auth"])
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")



@router.post("/login")
def login(user_data :UserLogin,
          db:Session=Depends(get_db)):

       user= db.query(User).filter(User.email ==user_data.email).first()

       if not user:
              raise HTTPException(
                     status_code=401,
                     detail="Invalid email or password"
              )
       if not verify_password(
              user_data.password,
              user.password
       ):
              raise HTTPException(
                     status_code=401,
                     detail="Invalid email or password"
              )

       access_token = create_access_token({
              "sub":str(user.id),
              "role":user.role
       })

       refresh_token = create_refresh_token({
        "sub": str(user.id)
       })


       return {
              "message":"Login successful",
              "user_id":user.id,
              "access_token": access_token,
              "refresh_token": refresh_token,
              "token_type": "bearer"
       }



@router.post("/refresh")
def refresh_access_token(refresh_token:str):

       try:
           payload = jwt.decode(
              refresh_token,
              SECRET_KEY,
              algorithms=[ALGORITHM]  
           )
           
           if payload.get("type") != "refresh":
               raise HTTPException(
                     status_code=401,
                     detail="Invalid refresh token "
               )
           user_id = payload.get("sub")

           if user_id is None :
              raise HTTPException(
                     status_code=401,
                     detail="Invalid refresh token"
              )
           access_token = create_access_token({
              "sub":str(user_id)
            })
           return{
              "access_token":access_token,
              "token_type":"bearer"
            }
       except JWTError:
             raise HTTPException(
                   status_code=401,
                   detail="Invalid or expired refresh token"
             )

@router.post("/reset-password")
def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    # Find user using reset token
    user = db.query(User).filter(
        User.reset_token == token
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token"
        )

    # Check token expiry
    if (
        not user.reset_token_expires
        or user.reset_token_expires < datetime.utcnow()
    ):
        raise HTTPException(
            status_code=400,
            detail="Reset token has expired"
        )

    # Hash new password
    user.password = hash_password(new_password)

    # Remove reset token
    user.reset_token = None
    user.reset_token_expires = None

    db.commit()

    return {
        "message": "Password reset successfully"
    }


@router.post("/forgot-password")
def forgot_password(
    email: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Generate secure token
    reset_token = secrets.token_urlsafe(32)

    # Token expiry: 15 minutes
    expires_at = datetime.utcnow() + timedelta(minutes=15)

    user.reset_token = reset_token
    user.reset_token_expires = expires_at

    db.commit()

    # Normally yahan email send karenge
    reset_link = f"http://localhost:3000/reset-password?token={reset_token}"

    return {
        "message": "Password reset link sent",
        "reset_link": reset_link
    }