from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import CHANNEL_URL, REF_URL


class ClientKeyboard:

    async def start_keyboard():
        ikb = InlineKeyboardBuilder()

        ikb.button(text="Подписаться", url=CHANNEL_URL)
        ikb.button(text="Проверить", callback_data="check")

        ikb.adjust(1)

        return ikb.as_markup()

    async def menu_keyboard():
        ikb = InlineKeyboardBuilder()

        ikb.button(text="📱Регистрация", callback_data="register")
        ikb.button(text="📚Инструкция", callback_data="instruction")
        ikb.button(text="💣Получить сигнал💣", callback_data="get_signal")

        ikb.adjust(2, 1)

        return ikb.as_markup()

    async def register_keyboard():
        ikb = InlineKeyboardBuilder()

        ikb.button(text="📱🔸 Зарегестрироваться", url=REF_URL)
        ikb.button(text="🔙Вернуться в главное меню",
                   callback_data="back")

        ikb.adjust(1)

        return ikb.as_markup()

    async def on_register_keyboard():
        ikb = InlineKeyboardBuilder()

        ikb.button(text="📚Инструкция", callback_data="instruction")
        ikb.button(text="💣Получить сигнал💣", callback_data="get_signal")
        ikb.button(text="🔙Вернуться в главное меню",
                   callback_data="back")

        ikb.adjust(2, 1)

        return ikb.as_markup()

    async def back_keyboard():
        ikb = InlineKeyboardBuilder()
        ikb.button(text="🔙Вернуться в главное меню",
                   callback_data="back")

        return ikb.as_markup()

    async def mines_keyboard():
        ikb = InlineKeyboardBuilder()
        ikb.button(text="1",
                   callback_data="one")
        ikb.button(text="3",
                   callback_data="three")
        ikb.button(text="5",
                   callback_data="five")
        ikb.button(text="7",
                   callback_data="sever")

        return ikb.as_markup()

    async def get_signal_keyboard():
        ikb = InlineKeyboardBuilder()

        ikb.button(text="💣Получить сигнал💣", callback_data="get_signal_again")
        ikb.button(text="🔙Вернуться в главное меню",
                   callback_data="back")

        ikb.adjust(1)

        return ikb.as_markup()
