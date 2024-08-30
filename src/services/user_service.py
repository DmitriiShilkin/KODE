import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import crud_user
from models.user import User
from schemas.user import UserCreate, UserCreateDB
from security.password import hash_password


async def create_user(db: AsyncSession, create_data: UserCreate) -> User:
    try:
        create_data = create_data.model_dump(exclude_unset=True)
        hashed_password = await hash_password(create_data.pop("password"))
        random_uid = str(uuid.uuid4())
        user_created = await crud_user.create(
            db=db,
            create_schema=UserCreateDB(
                uid=random_uid,
                username=random_uid,
                hashed_password=hashed_password,
                **create_data,
                commit=False,
            ),
        )
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    return user_created
