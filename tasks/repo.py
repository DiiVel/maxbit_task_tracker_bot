from collections.abc import Sequence
from typing import Any
from loguru import logger

from sqlalchemy import delete, insert, or_, select

from tg_task_tracker.database import AsyncSessionFactory
from tasks.models import Task
from tasks.schema import TaskCreate


class TaskRepo(AsyncSessionFactory):
    def __init__(self, *args: Any, **kwargs: dict[str, Any]):
        super().__init__(*args, **kwargs)

    async def get_tasks(self, *_: Any, **filters: dict[str, Any]) -> Sequence[Task]:
        """
        Method that returns all tasks in the database
        :param _: any argument
        :param filters: filters by which tasks should be returned
        :return: sequence of tasks
        """
        stmt = select(Task)

        filter_set = [
            getattr(Task, attr) == value
            for attr, value in filters.items()
            if hasattr(Task, attr)
        ]

        if filter_set:
            stmt = stmt.filter(or_(*filter_set))

        session = await super().get_session()
        data = (await session.execute(stmt)).scalars().fetchall()
        await session.close()
        return data

    async def get_task(self, task_id: int) -> Task | None:
        """
        Method that returns task with given id
        :param task_id: Task id
        :return: Task or None
        """
        stmt = select(Task).where(Task.id == task_id)

        session = await super().get_session()
        data = (await session.execute(stmt)).scalar_one_or_none()
        await session.close()
        return data

    async def create_task(self, data: TaskCreate) -> Task | None:
        """
        Method that creates a new task by given data
        :param data: Data to create new task
        :return: Task, that was created, or None if task already exists or if task was not created
        """
        stmt = (
            insert(Task)
            .values(title=data.title, description=data.description, status=data.status)
            .returning(Task)
        )

        session = await super().get_session()
        try:
            task = (await session.execute(stmt)).scalar_one_or_none()
            await session.commit()
            return task
        except Exception as e:
            logger.exception(e)
        finally:
            await session.close()

    async def delete_task(self, task_id: int) -> None:
        """
        Method that deletes user with given id
        :param task_id: Task id
        :return: None
        """
        stmt = delete(Task).where(Task.id == task_id)

        session = await super().get_session()
        await session.execute(stmt)
        await session.commit()
        await session.close()
