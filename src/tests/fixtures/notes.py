import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from crud.note import crud_note
from models import Note, User
from schemas.note import NoteCreateDB


@pytest_asyncio.fixture
async def note_fixture(
    async_session: AsyncSession, user_fixture: User
) -> Note:
    schema = NoteCreateDB(
        text="Test note text",
        author_id=user_fixture.id,
    )
    new_note = await crud_note.create(
        db=async_session,
        create_schema=schema,
    )

    await async_session.commit()
    return new_note


@pytest_asyncio.fixture
async def note_fixture_2(
    async_session: AsyncSession, user_fixture: User
) -> Note:
    schema = NoteCreateDB(
        text="Test another note text",
        author_id=user_fixture.id,
    )
    new_note = await crud_note.create(
        db=async_session,
        create_schema=schema,
    )

    await async_session.commit()
    return new_note
