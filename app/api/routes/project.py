from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
from app.models.project import Project
from app.models.user import User
from app.api.deps import get_session, require_role
from app.schemas.project import ProjectCreate, ProjectRead

router = APIRouter(prefix="/projects", tags=["Projects"])

# Create a new project for 'Admin' role only
@router.post("/", response_model=ProjectRead)
async def create_project(
    project_in: ProjectCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_role(["admin"]))
):
    project = Project(
        **project_in.model_dump(),
        created_by=current_user.id
    )
    # project.created_by = current_user.id
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project

# Read all rows of Project Table for any role (admin or user)
@router.get("/", response_model=list[ProjectRead])
async def list_projects(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_role(["admin", "user"]))
):
    result = await session.exec(select(Project))
    return result.all()

# Delete the row in Project Table with given project_id
@router.delete("/{project_id}")
async def delete_project(
    project_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_role(["admin"]))
):
    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    await session.delete(project)
    await session.commit()
    return {"detail": "Project deleted"}
