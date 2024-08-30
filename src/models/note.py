from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Note(Base):
    """
    Модель заметки

    ## Attrs
        - id: int - идентификатор заметки
        - text: str - текст заметки
        - created_at: datetime - дата и время создания заметки
        - author_id: int - FK User - идентификатор автора заметки
        - author : User - связь пользователь автор заметки
    """

    __tablename__ = "note"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="CASCADE")
    )
    author: Mapped["User"] = relationship(
        "User", back_populates="notes"
    )

    def __repr__(self) -> str:
        return f"{self.id} {self.author_id}"
