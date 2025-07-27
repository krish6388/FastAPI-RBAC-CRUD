from pydantic import BaseModel
from typing import Optional

"""
    This file include schemas for User table
"""

class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"


class UserRead(BaseModel):
    id: str
    username: str
    role: str
