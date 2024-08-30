from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from crud.crud_mixins import BaseCRUD, CreateAsync, ReadAsync
from schemas.note import NoteCreateDB
from models import Note


class CRUDNote(
    BaseCRUD[Note],
    CreateAsync[Note, NoteCreateDB],
    ReadAsync[Note],
):
    async def get_by_id(
        self,
        db: AsyncSession,
        obj_id: int,
    ) -> Optional[Note]:
        statement = (
            select(self.model)
            .options(
                joinedload(self.model.author),
            )
            .where(self.model.id == obj_id)
        )
        result = await db.execute(statement)
        return result.scalars().first()

    async def get_multi(
            self,
            db: AsyncSession,
            user_id: int,
            skip: int,
            limit: int,
    ) -> List[Note]:
        statement = (
            select(self.model)
            .where(
                self.model.author_id == user_id,
            )
            .options(joinedload(self.model.author))
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(statement)
        return result.scalars().all()


crud_note = CRUDNote(Note)
