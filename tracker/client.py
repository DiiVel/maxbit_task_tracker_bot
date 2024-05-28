from typing import Any

from loguru import logger
from pyrogram.client import Client


class Tracker(Client):
    client_name = "tracker"

    def __init__(
            self,
            api_id: int,
            api_hash: str,
            bot_token: str,
            *args: Any,
            **kwargs: dict[str, Any],
    ) -> None:
        super().__init__(name=Tracker.client_name, api_hash=api_hash, api_id=api_id, bot_token=bot_token, *args,
                         **kwargs)

    async def start(self) -> None:
        logger.info("Tracker client just started")
        await super().start()

    async def stop(self, *args: Any, **kwargs: dict[str, Any]) -> None:
        logger.info("Tracker client just stopped")
        await super().stop(*args, **kwargs)
