from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.database import get_async_db
from crud.user import crud_user
from schemas.user import (
    UserCreate,
    UserResponse,
)
from services import user_service

router = APIRouter()


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    create_data: UserCreate,
    db: AsyncSession = Depends(get_async_db),
):
    user = await crud_user.get_by_email(db, email=create_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {create_data.email} is already "
            "associated with an account.",
        )
    new_user = await user_service.create_user(db=db, create_data=create_data)
    return new_user
