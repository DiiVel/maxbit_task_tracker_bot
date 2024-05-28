from collections.abc import Sequence

from datetime import datetime
from typing import Any

from users.repo import UserRepo
from users.schema import UserCreate, UserResponse


class UserService(UserRepo):
    def __init__(self, *args: Any, **kwargs: dict[str, Any]):
        super().__init__(*args, **kwargs)

    # async def get_newbies_for_today(self) -> Sequence[UserResponse]:
    #     today = datetime.today().date()
    #
    #     users = await super().get_users()
    #     fetched_users = (UserResponse.model_validate(data) for data in users)
    #
    #     return [user for user in fetched_users if user.created_at.date() == today]

    async def get_users(self) -> Sequence[UserResponse]:
        users = await super().get_users()
        return [UserResponse.model_validate(data) for data in users]

    async def get_user_by_telegram_id(self, user_telegram_id: int) -> UserResponse | None:
        user = await super().get_user(user_telegram_id=user_telegram_id)
        if user is None:
            return None
        return UserResponse.model_validate(user)

    async def create_user(self, data: UserCreate) -> UserResponse | None:
        user = await super().create_user(data)
        if user is None:
            return None
        return UserResponse.model_validate(user)

    async def delete_user(self, user_id: int) -> None:
        await super().delete_user(user_id=user_id)
