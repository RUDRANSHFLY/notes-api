from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
