from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from crud.async_crud import BaseAsyncCRUD
from models import User
from schemas.user import UserCreateDB, UserUpdateDB


class CRUDUser(BaseAsyncCRUD[User, UserCreateDB, UserUpdateDB]):
    async def get_by_uid(
        self, db: AsyncSession, *, uid: UUID
    ) -> Optional[User]:
        statement = (
            select(self.model)
            .where(self.model.uid == uid)
            .options(
                joinedload(self.model.notes),
            )
        )
        result = await db.execute(statement)
        return result.scalars().first()

    async def get_by_email(
        self, db: AsyncSession, *, email: str
    ) -> Optional[User]:
        statement = (
            select(self.model)
            .where(self.model.email == email)
        )
        result = await db.execute(statement)
        return result.scalars().first()

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: User,
        update_data: Union[UserUpdateDB, dict],
        commit: bool = True,
    ) -> User:
        if isinstance(update_data, BaseModel):
            update_data = update_data.model_dump(exclude_unset=True)

        stmt = (
            update(self.model)
            .where(self.model.id == db_obj.id)
            .values(**update_data)
            .returning(self.model)
            .options(
                joinedload(self.model.notes),
            )
        )
        result = await db.execute(stmt)
        obj = result.scalars().first()
        if commit:
            await db.commit()
            await db.refresh(obj)
        return obj


crud_user = CRUDUser(User)
