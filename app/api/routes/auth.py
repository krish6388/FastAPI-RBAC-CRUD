from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.schemas.user import UserCreate, UserRead
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.api.deps import get_session
# from app.core.security import verify_password, create_access_token
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.core.config import get_settings


router = APIRouter()

@router.post("/register", response_model=UserRead)
async def register_user(
    user_create: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    # Check if the user already exists
    result = await session.exec(select(User).where(User.username == user_create.username))
    existing_user = result.first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered."
        )

    # Create and hash the password
    user = User(
        username=user_create.username,
        hashed_password=hash_password(user_create.password),
        role=user_create.role
    )

    # Save the new user
    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Return only safe, public data
    return UserRead(id=str(user.id), username=user.username, role=user.role)

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    # Find the user by username
    result = await session.exec(select(User).where(User.username == form_data.username))
    user = result.first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Create token payload
    access_token_expires = timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
