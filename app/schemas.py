import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class PostResponse(PostBase):
    id: int
    created_at: datetime.datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True
    

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class tokenData(BaseModel):
    user_id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: int

class PostOut(BaseModel):
    post: PostResponse
    votes: int
    class Config:
        from_attributes = True
