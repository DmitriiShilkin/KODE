from typing import Generic, Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from constants.crud_types import ModelType


class ReadAsync(Generic[ModelType]):
    async def get(self, db: AsyncSession, obj_id: int) -> Optional[ModelType]:
        return await db.get(self.model, obj_id)

    async def get_by_id(
        self, db: AsyncSession, *, obj_id: int
    ) -> Optional[ModelType]:
        statement = select(self.model).where(self.model.id == obj_id)
        result = await db.execute(statement)
        return result.scalars().first()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[ModelType]:
        statement = (
            select(self.model)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(statement)
        return result.scalars().all()
