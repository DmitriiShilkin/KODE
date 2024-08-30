from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies.auth import get_current_user
from api.dependencies.database import get_async_db
from crud.note import crud_note
from models import User
from schemas.note import (
    NoteCreate,
    NoteCreateDB,
    NoteResponse,
)


router = APIRouter()


@router.get("/", response_model=List[NoteResponse])
async def read_notes(
    db: Session = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    return await crud_note.get_multi(
        db=db, user_id=current_user.id,
        skip=skip,
        limit=limit
    )


@router.post(
    "/",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_note(
    create_data: NoteCreate,
    db: Session = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    schema = NoteCreateDB(
        author_id=current_user.id,
        **create_data.model_dump(),
    )
    try:
        new_note = await crud_note.create(
            db=db, create_schema=schema
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    return await crud_note.get_by_id(db=db, obj_id=new_note.id)
