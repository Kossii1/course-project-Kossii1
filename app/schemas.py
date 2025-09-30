from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class WorkoutBase(BaseModel):
    date: str
    note: Optional[str] = ""


class WorkoutCreate(WorkoutBase):
    pass


class WorkoutUpdate(BaseModel):
    date: Optional[str] = None
    note: Optional[str] = None


class WorkoutOut(WorkoutBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
