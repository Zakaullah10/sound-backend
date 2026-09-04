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
              full_name=user.full_name,
              username=user.username,
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

       user.full_name=user_data.full_name,
       user.username=user_data.username,
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
