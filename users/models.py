from datetime import datetime

from sqlalchemy import String, text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
import uuid

from tg_task_tracker.database import Base
from tasks.models import Task


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    )

    user_telegram_id: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
        unique=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
    )

    username: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
        unique=True,
    )

    name: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
        unique=False,
    )

    tasks: Mapped[list["Task"]] = relationship("Task", backref="user")
