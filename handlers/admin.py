from aiogram import F, Router, types, Bot
from aiogram.filters.command import CommandStart
from keyboards.admin import admin_command
from database.db import DataBase
from aiogram.fsm.context import FSMContext
from database.db import DataBase
from config import ADMIN_ID



from aiogram.fsm.state import State, StatesGroup
class Admin_States(StatesGroup):
    #give balance(выдача баланса)
    
    get_userinfo = State()
    give_balance = State()
    
    #delete balance(удаление баланса)

    get_userinfo_del = State()
    delete_balance = State()

    #mailing(рассылка)

    mailing_text = State()


router = Router()


@router.message(F.text == '/admin')
async def admin_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        await state.clear()
        users_count = await DataBase.get_users()
        money_list = await DataBase.get_users()
        money_count = 0


        await message.answer("Добро пожаловать", reply_markup=await admin_command(), parse_mode="HTML")


@router.callback_query(F.data == 'mailing')
async def mailing_state(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer("Отправьте сообщение")
    await state.set_state(Admin_States.mailing_text)


@router.message(Admin_States.mailing_text)
async def mailing_state(message: types.Message, state: FSMContext, bot: Bot):
    mailing_message = message.message_id
    ikb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Отправить', callback_data='send_mailing'), types.InlineKeyboardButton(
            text='Отмена', callback_data='decline_mailing')]
    ])
    await bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id,
                           message_id=mailing_message, reply_markup=ikb, parse_mode="HTML")

    await state.update_data(msg=mailing_message)


@router.callback_query(F.data == 'send_mailing')
async def mailing_handler(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    errors_count = 0
    good_count = 0
    data = await state.get_data()
    mailing_message = data['msg']
    users = await DataBase.get_users()
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer("Рассылка начата...")
    for i in users:
        try:
            await bot.copy_message(chat_id=i[1], from_chat_id=callback.from_user.id,
                                   message_id=mailing_message, parse_mode="HTML")
            good_count += 1
        except Exception as ex:
            errors_count += 1
            print(ex)

    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer(f"<b>Кол-во отосланных сообщений:</b> <code>{good_count}</code>\n\
<b>Кол-во пользователей заблокировавших бота:</b> <code>{errors_count}</code>", parse_mode="HTML")
    await callback.answer()
    await state.clear()


@router.callback_query(F.data == 'decline_mailing')
async def decline_mailing(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer("Рассылка отменена", reply_markup=await admin_command())
    await state.clear()
