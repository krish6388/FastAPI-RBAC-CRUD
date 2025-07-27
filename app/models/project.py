from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime

# Model for Project Table
class Project(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    title: str
    description: Optional[str] = None
    created_by: UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationship (optional for backref)
    # tasks: list["Task"] = Relationship(back_populates="project")
