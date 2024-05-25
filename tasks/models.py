import enum
from datetime import datetime
from sqlalchemy import String, text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, ENUM, TIMESTAMP
import uuid

from tg_task_tracker.database import Base
from users.models import User


class TaskStatus(str, enum.Enum):
    done = "done"
    in_progress = "in_progress"
    not_started = "not_started"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    )

    status: Mapped[TaskStatus] = mapped_column(
        ENUM(TaskStatus, name="task_status_enum"),
        nullable=False,
        default=TaskStatus.not_started
    )

    title: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
        unique=False,
    )

    description: Mapped[str] = mapped_column(
        String(512),
        nullable=True,
        unique=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )
    user: Mapped["User"] = relationship(backref="tasks")
