from pyrogram import filters
from pyrogram.handlers.message_handler import MessageHandler

from tg_task_tracker.config import cfg
from tracker.client import Tracker
from tracker.handlers import start, handle_name, handle_username
from tracker.states import RegistrationStates

client = Tracker(
    api_id=cfg.api_id,
    api_hash=cfg.api_hash,
    bot_token=cfg.bot_token,
)

client.add_handler(
    MessageHandler(
        start,
        filters.command("start"),
    ),
)

client.add_handler(
    MessageHandler(
        handle_name,
        filters.text  # & filters.state(RegistrationStates.NAME),
    ),
)

client.add_handler(
    MessageHandler(
        handle_username,
        filters.text  # & filters.state(RegistrationStates.USERNAME),
    ),
)
