from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # converts properly an orm object
    class Config:
        from_attributes = True


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut

    # converts properly an orm object
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    user_id: int
    post_id: int
    dir: int
