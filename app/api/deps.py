from typing import Callable
from app.db.session import async_session
from sqlmodel.ext.asyncio.session import AsyncSession
from collections.abc import AsyncGenerator
from fastapi import Depends
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.db.session import async_session
from app.models.user import User

# Catch access token from Auth header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Yields a new db session for db interaction and self clean-up
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# Takes JWT from Auth header -> decode it -> maps with its user_id
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session)
) -> User:
    payload = decode_access_token(token)
    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload invalid"
        )

    result = await session.exec(select(User).where(User.id == user_id))
    user = result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user

# RBAC setup -> Can be re-used for multiple tables
def require_role(roles: list[str]) -> Callable:
    async def role_dependency(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this resource"
            )
        return current_user
    return role_dependency

