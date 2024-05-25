from collections.abc import Sequence
from typing import Any
from loguru import logger

from sqlalchemy import delete, insert, or_, select

from tg_task_tracker.database import AsyncSessionFactory
from users.models import User
from users.schema import UserCreate


class UserRepo(AsyncSessionFactory):
    def __init__(self, *args: Any, **kwargs: dict[str, Any]):
        super().__init__(*args, **kwargs)

    async def get_users(self, *_: Any, **filters: dict[str, Any]) -> Sequence[User]:
        """
        Method that returns all users in the database
        :param _: any argument
        :param filters: filters by which users should be returned
        :return: sequence of users
        """
        stmt = select(User)

        filter_set = [
            getattr(User, attr) == value
            for attr, value in filters.items()
            if hasattr(User, attr)
        ]

        if filter_set:
            stmt = stmt.filter(or_(*filter_set))

        session = await super().get_session()
        data = (await session.execute(stmt)).scalars().fetchall()
        await session.close()
        return data

    async def get_user(self, user_id: int) -> User | None:
        """
        Method that returns user with given id
        :param user_id: User id
        :return: User or None
        """
        stmt = select(User).where(User.id == user_id)

        session = await super().get_session()
        data = (await session.execute(stmt)).scalar_one_or_none()
        await session.close()
        return data

    async def create_user(self, data: UserCreate) -> User | None:
        """
        Method that creates a new user by given data
        :param data: Data to create new user
        :return: User, that was created, or None if user already exists or if user was not created
        """
        stmt = (
            insert(User)
            .values(user_telelegram_id=data.user_telegram_id, username=data.username, name=data.name)
            .returning(User)
        )

        session = await super().get_session()
        try:
            user = (await session.execute(stmt)).scalar_one_or_none()
            await session.commit()
            return user
        except Exception as e:
            logger.exception(e)
        finally:
            await session.close()

    async def delete_user(self, user_id: int) -> None:
        """
        Method that deletes user with given id
        :param user_id: User id
        :return: None
        """
        stmt = delete(User).where(User.id == user_id)

        session = await super().get_session()
        await session.execute(stmt)
        await session.commit()
        await session.close()
