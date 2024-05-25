from collections.abc import Sequence

from datetime import datetime
from typing import Any

from tasks.repo import TaskRepo
from tasks.schema import TaskCreate, TaskResponse


class TaskService(TaskRepo):
    def __init__(self, *args: Any, **kwargs: dict[str, Any]):
        super().__init__(*args, **kwargs)

    # async def get_newbies_for_today(self) -> Sequence[UserResponse]:
    #     today = datetime.today().date()
    #
    #     users = await super().get_users()
    #     fetched_users = (UserResponse.model_validate(data) for data in users)
    #
    #     return [user for user in fetched_users if user.created_at.date() == today]

    async def get_tasks(self) -> Sequence[TaskResponse]:
        tasks = await super().get_tasks()
        return [TaskResponse.model_validate(data) for data in tasks]

    async def get_task_by_id(self, task_id: int) -> TaskResponse | None:
        task = await super().get_task(task_id=task_id)
        if task is None:
            return None
        return TaskResponse.model_validate(task)

    async def create_user(self, data: TaskCreate) -> TaskResponse | None:
        user = await super().create_task(data)
        if user is None:
            return None
        return TaskResponse.model_validate(user)

    async def delete_user(self, task_id: int) -> None:
        await super().delete_task(task_id=task_id)
