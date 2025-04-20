from aiogram.utils.keyboard import InlineKeyboardBuilder

async def admin_command():
    ikb = InlineKeyboardBuilder()

    ikb.button(text="Рассылка📩", callback_data="mailing")
    ikb.adjust(1, 2)
    return ikb.as_markup()

