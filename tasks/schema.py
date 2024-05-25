from datetime import datetime

from tg_task_tracker.schema import BaseSchema
from tasks.models import TaskStatus


class TaskCreate(BaseSchema):
    """
    Task creation schema definition
    """
    title: str
    description: str | None
    status: TaskStatus = TaskStatus.not_started


class TaskResponse(TaskCreate):
    """
    Task response schema definition
    """
    id: int
    created_at: datetime
    updated_at: datetime
    status: TaskStatus
    created_at: datetime
    updated_at: datetime