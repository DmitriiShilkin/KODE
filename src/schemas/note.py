from datetime import datetime

from pydantic import BaseModel, Field

from constants.note import MAX_LENGTH_TEXT, MIN_LENGTH_TEXT
from schemas.user import UserNoteResponse


class NoteBase(BaseModel):
    text: str = Field(min_length=MIN_LENGTH_TEXT, max_length=MAX_LENGTH_TEXT)

    class Config:
        from_attributes = True


class NoteCreate(NoteBase):
    ...


class NoteCreateDB(NoteBase):
    author_id: int


class NoteResponseBase(NoteBase):
    created_at: datetime


class NoteResponse(NoteResponseBase):
    author: UserNoteResponse
