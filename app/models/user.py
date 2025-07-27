from sqlmodel import SQLModel, Field
from typing import Optional
import uuid

# Model for User Table
class User(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    role: str = Field(default="user")
