from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

"""
    This file include schemas for Project table
"""

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectRead(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    created_by: UUID
    created_at: datetime

    class Config:
        orm_mode = True
