from datetime import datetime

from tg_task_tracker.schema import BaseSchema


class UserCreate(BaseSchema):
    """
    User creation schema definition
    """
    user_telegram_id: str
    username: str
    name: str


class UserResponse(UserCreate):
    """
    User response schema definition
    """
    id: int
    created_at: datetime
    name: str
    username: str