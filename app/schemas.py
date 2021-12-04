from typing import Optional
from pydantic import BaseModel
from pydantic.networks import EmailStr
from sqlalchemy.sql.sqltypes import DateTime
from datetime import datetime
from pydantic.types import conint
from app.database import Base

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    # rating: Optional[int] = None

class CreatePost(BaseModel):
    title : str
    content : str
    published : bool = True
    

class UpdatePost(BaseModel):
    title : str
    content : str
    published : bool
class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        orm_mode = True


class PostResponse(BaseModel):
    id:int
    title:str
    content:str
    published:bool
    user_id:int
    created_at:datetime
    owner:UserResponse
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes:int
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email:EmailStr
    password:str


class UserLogin(BaseModel):
    email:EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str] = None
    # created_at: datetime

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

# get users by vote
