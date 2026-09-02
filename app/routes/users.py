from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.security import hash_password,verify_password,create_access_token,create_refresh_token
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate,UserRespose,UserLogin
from app.dependencies.auth import get_current_user,get_current_admin
from jose import jwt , JWTError
import secrets
from datetime import  datetime , timedelta
import os


router = APIRouter(tags=["Users"])
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

@router.post("/user" , response_model=UserRespose)
def create_user(
    user:UserCreate,
    db:Session=Depends(get_db)
    ):
       existing_user = db.query(User).filter(
              User.email ==  user.email
       ).first()

       if existing_user:raise HTTPException(
              status_code=409,
              detail="Email already registered"
       )

       hashed_password = hash_password(user.password)
       new_user= User(
               name=user.name,
              email = user.email,
              password = hashed_password,
              role = user.role
       )
       print(new_user)
       db.add(new_user)
       db.commit()
       db.refresh(new_user)

       return new_user

@router.get("/users", response_model=list[UserRespose])
def get_users(db:Session = Depends(get_db)):
       users = db.query(User).all()
       return users

@router.get("/users/{user_id}",response_model=UserRespose)
def get_user(user_id:int, db:Session=Depends(get_db)):

       user=db.query(User).filter(User.id == user_id).first()

       if not user:
              raise HTTPException(
                     status_code =404,
                     details="User not found"
              )
       return user

@router.put("/users/{user_id}",response_model=UserRespose)
def update_user(
       user_id: int,
       user_data:UserCreate,
       db:Session=Depends(get_db)
):
       user = db.query(User).filter(User.id == user_id).first()

       if not user:
              raise HTTPException(
                     status_code=404,
                     detail="User not found"
              )

       user.name= user_data.name
       user.email= user_data.email
       user.password = hash_password(user_data.password)

       db.commit()
       db.refresh(user)

       return user


@router.delete("/users/{user_id}")
def delete_user(
       user_id:int,
       db:Session=Depends(get_db)
):
       user = db.query(User).filter(User.id == user_id).first()

       if not user :
              raise HTTPException(
                     status_code=404,
                     detail="User not found"
              )
       db.delete(user)
       db.commit()

       return {
              "message":"User deleted successfully"
       }

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



@router.get("/profile", response_model=UserRespose)
def get_profile (
       current_user : User = Depends(get_current_user)
):return current_user


@router.get("/admin/users", response_model=list[UserRespose])
def get_all_users(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return db.query(User).all()

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