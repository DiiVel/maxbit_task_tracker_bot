from pyrogram import Client, types

from states import RegistrationStates
from users.service import UserService
from users.schema import UserCreate


async def start(client: Client, message: types.Message):
    user_telegram_id = message.from_user.id
    user = await UserService().get_user_by_telegram_id(user_telegram_id=user_telegram_id)
    if user:
        await message.reply(f"Привет, {user.name}! Рады видеть вас снова.")
        return
    else:
        await message.reply("Привет! Давай зарегистрируемся. Введи свое имя:")
        return RegistrationStates.NAME


async def handle_name(client: Client, message: types.Message, state):
    name = message.text
    state[RegistrationStates.NAME] = name
    await message.reply(
        text="Отлично! Теперь выбери уникальный логин:",
        reply_markup=create_username_menu(telegram_username=message.from_user.username)
    )
    return RegistrationStates.USERNAME


async def handle_username(client: Client, message: types.Message, state):
    user_telegram_id = message.from_user.id
    username = message.text
    state[RegistrationStates.USERNAME] = username

    data = UserCreate(
        telegram_user_id=user_telegram_id,
        username=username,
        name=state[RegistrationStates.NAME]
    )
    await UserService().create_user(data=data)

    await message.reply(
        f"Регистрация завершена! Ваши данные:\nИмя: {state[RegistrationStates.NAME]}\nЛогин: {username}"
    )
    return None


def create_username_menu(telegram_username):
    buttons = [
        [types.InlineKeyboardButton("Использовать Telegram username", callback_data="use_telegram_username")],
        [types.InlineKeyboardButton("Ввести новый username", switch_inline_query_current_chat="")]
    ]
    if telegram_username:
        buttons.insert(0, [
            types.InlineKeyboardButton(f"Использовать {telegram_username}", callback_data=f"use_{telegram_username}")])
    return types.InlineKeyboardMarkup(buttons)
