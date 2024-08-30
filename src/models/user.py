import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression, func

from .base import Base

if TYPE_CHECKING:
    from .note import Note


class User(Base):
    """
    Модель пользователя

    ## Attrs
        - id: int - идентификатор пользователя
        - uid: UUID - уникальный идентификаторпользователя
        - first_name: str - имя пользователя
        - second_name: str - фамилия пользователя
        - username: str - юзернейм пользователя
        - email: str - адрес электронной почты пользователя
        - hashed_password: str - зашифрованный пароль пользователя
        - is_email_verified: bool - признак наличия подтверждения email пользователя
        - is_admin: bool - признак наличия прав администратора
        - is_superuser: bool - признак наличия прав суперпользователя
        - registered_at: datetime - дата и время регистрации пользователя
        - updated_at: datetime - дата и время изменения пользователя
        - last_visited_at: datetime - дата и время последнего визита пользователя
        - last_password_change_at: datetime - дата и время последнего изменения пароля пользователя
        - notes: Note - связь пользователя с заметками
    """
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    uid: Mapped[uuid.UUID] = mapped_column(
        UUID, unique=True, index=True, default=uuid.uuid4
    )
    first_name: Mapped[str]
    second_name: Mapped[str]
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=True)
    is_email_verified: Mapped[bool] = mapped_column(
        Boolean, server_default=expression.false()
    )
    is_admin: Mapped[bool] = mapped_column(
        Boolean, server_default=expression.false()
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, server_default=expression.false()
    )
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    last_visited_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )
    last_password_change_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    notes: Mapped[list["Note"]] = relationship(
        "Note", back_populates="author"
    )

    @property
    def fullname(self) -> str:
        return f"{self.second_name} {self.first_name}"

    def __str__(self) -> str:
        return f"{self.id} - {self.fullname}"
