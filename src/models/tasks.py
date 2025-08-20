from datetime import datetime
import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base
from src.utils.structs import Status


class Tasks(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[Status]
    date: Mapped[datetime] = mapped_column(default=datetime.now())
