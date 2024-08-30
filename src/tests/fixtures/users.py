import uuid

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import crud_user
from models.user import User
from schemas.user import UserCreateDB
from security.password import hash_password


@pytest_asyncio.fixture
async def user_fixture(async_session: AsyncSession) -> User:
    unique_username = f"Existing_user_{uuid.uuid4()}"
    unique_email = f"test_user_{uuid.uuid4()}@test.com"
    schema = UserCreateDB(
        uid=uuid.uuid4(),
        username=unique_username,
        first_name="Existing",
        second_name="User",
        email=unique_email,
        hashed_password=await hash_password("password"),
    )
    new_user = await crud_user.create(db=async_session, create_schema=schema)
    return new_user


@pytest_asyncio.fixture
async def user_fixture_2(async_session: AsyncSession) -> User:
    schema = UserCreateDB(
        uid=uuid.uuid4(),
        username="Another_user",
        first_name="Another",
        second_name="User",
        email="test_user_another@test.com",
        hashed_password=await hash_password("password"),
    )
    new_user = await crud_user.create(db=async_session, create_schema=schema)
    return new_user
