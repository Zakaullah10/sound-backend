from pydantic import BaseModel,EmailStr,Field

class UserCreate (BaseModel):
    name:str = Field(min_length=5 , max_length=50)
    email:EmailStr
    password :str = Field(min_length=6 , max_length=72)
    role :str


class UserRespose(BaseModel):
    id:int
    name:str
    email:str
    role :str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email:str
    password:str
    

