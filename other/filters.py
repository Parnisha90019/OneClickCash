from aiogram import types
from aiogram.filters import BaseFilter
from config import CHANNEL_ID
from database.db import DataBase

class ChatJoinFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        try:
            member = await message.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)
            return member.status != 'left'
        except:
            return False

class RegisteredFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return bool(await DataBase.get_user(message.from_user.id))

class DepositFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return bool(await DataBase.has_deposited(message.from_user.id))