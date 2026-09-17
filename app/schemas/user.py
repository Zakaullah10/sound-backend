from pydantic import BaseModel,EmailStr,Field

class UserCreate (BaseModel):
    full_name:str = Field(min_length=2 , max_length=50)
    username:str = Field(min_length=2 , max_length=50)
    email:EmailStr
    password :str = Field(min_length=6 , max_length=72)
    role :str


class UserRespose(BaseModel):
    id:int
    full_name:str
    username:str
    email:str
    role :str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email:str
    password:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    REFRESH_TOKEN_EXPIRE_MINUTES:int

    class Config:
        from_attributes = True

class UserRefreshToken(BaseModel):
    refresh_token:str

    class Config:
        from_attributes = True

