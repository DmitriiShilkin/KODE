import logging
from datetime import datetime, UTC
from uuid import UUID

from fastapi import Depends, HTTPException, Security, status
from fastapi_jwt import JwtAuthorizationCredentials
from jose import JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from constants.auth import USER_ONLINE_DURATION_MINUTES
from crud.user import crud_user
from databases.database import get_async_session
from models import User
from schemas.token import TokenPayload
from security.token import access_security


async def get_current_user(
    credentials: JwtAuthorizationCredentials = Security(access_security),
    db: AsyncSession = Depends(get_async_session),
) -> User:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    try:
        token_user = TokenPayload(**credentials.subject)
    except (JWTError, ValidationError) as ex:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from ex
    return await get_user(db=db, user_uid=token_user.uid)


async def get_user(
    db: AsyncSession, user_uid: UUID
) -> User:
    user = await crud_user.get_by_uid(db, uid=user_uid)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    try:
        await update_last_visited_at(db=db, user=user)
    except Exception as ex:
        logging.exception(ex)  # noqa: TRY401
    return user


async def update_last_visited_at(db: AsyncSession, user: User) -> None:
    current_time = datetime.now(UTC)
    if not user.last_visited_at:
        await crud_user.update(
            db, db_obj=user, update_data={"last_visited_at": current_time}
        )
        return

    seconds_from_last_online = current_time - user.last_visited_at
    minutes_from_last_online = seconds_from_last_online.total_seconds() / 60
    if minutes_from_last_online > USER_ONLINE_DURATION_MINUTES:
        await crud_user.update(
            db, db_obj=user, update_data={"last_visited_at": current_time}
        )
