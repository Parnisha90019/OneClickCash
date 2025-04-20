import os
from random import choice, uniform, randint
import asyncio
import datetime

from aiogram import F, Router, types, Bot
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import CHANNEL_ID, REF_URL
from keyboards.client import ClientKeyboard
from other.filters import ChatJoinFilter, RegisteredFilter, DepositFilter
from database.db import DataBase

router = Router()

class RegisterState(StatesGroup):
    input_id = State()

class GetSignalStates(StatesGroup):
    chosing_mines = State()

@router.message(CommandStart())
async def start_command(message: types.Message, bot: Bot):
    await DataBase.register(message.from_user.id, verifed="0")
    await message.answer(f"""
Добро пожаловать, <b>{message.from_user.first_name}!</b>

Для использования бота - <b>подпишись</b> на наш канал🤝""",
                         reply_markup=await ClientKeyboard.start_keyboard(), parse_mode="HTML")

@router.callback_query(F.data.in_(["check", "back"]), ChatJoinFilter())
async def menu_output(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer("""
Добро пожаловать в 🔸<b>KanfiMines</b>🔸!

💣Mines - это гемблинг игра в букмекерской конторе 1win, которая основывается на классическом “Сапёре”.
Ваша цель - открывать безопасные ячейки и не попадаться в ловушки.

<code>Наш бот основан на нейросети от OpenAI.
Он может предугадать расположение звёзд с вероятностью 85%.</code>
❗️ ВНИМАНИЕ ❗️
Бот работает корректно, только с новыми аккаунтами (инструкция по регистрации есть ниже по кнопке)
❗️ ДЛЯ игры без риска ❗️
Нужен новый, чистый аккаунт, в котором при первом
депозите нужно ввести промокод MEMEZONA который даст +500% к депозиту (инструкция по кнопке ниже)""",
                                  parse_mode="HTML", reply_markup=await ClientKeyboard.menu_keyboard())
    await callback.answer()

@router.callback_query(F.data == "register")
async def register_handler(callback: types.CallbackQuery, state: FSMContext):
    text = f"""
🔷 1. Для начала зарегистрируйтесь по ссылке на сайте с ОБЯЗАТЕЛЬНЫМ использованием промокода MEMEZONA <a href="{REF_URL}">1WIN</a>
🔷 2. После успешной регистрации cкопируйте ваш айди на сайте (Вкладка 'пополнение' и в правом верхнем углу будет ваш ID).
🔷 3. И отправьте его боту в ответ на это сообщение!"""
    photo = types.FSInputFile("reg.jpg")

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(text, parse_mode="HTML", reply_markup=await ClientKeyboard.register_keyboard())
    await state.set_state(RegisterState.input_id)

@router.message(RegisterState.input_id)
async def register_handler_finaly(message: types.Message, state: FSMContext):
    try:
        user_id_1win = int(message.text)
        if len(message.text) >= 8:
            await DataBase.update_user_id_1win(message.from_user.id, user_id_1win)
            await message.answer("ID сохранён. Ожидайте подтверждения регистрации и депозита от 1win.", reply_markup=await ClientKeyboard.on_register_keyboard())
            await state.clear()
        else:
            await message.answer("Неверный ID")
            return
    except Exception as e:
        print(e)
        await message.answer("Неверный ID")
        return

@router.callback_query(F.data == "instruction", ChatJoinFilter())
async def instucrion_handler(callback: types.CallbackQuery):
    text = f"""
Бот основан и обучен на кластере нейросети 🖥 <strong>[KanfiMines]</strong>.
Для тренировки бота было сыграно 🎰10.000+ игр.

В данный момент пользователи бота успешно делают в день 15-25% от своего 💸 капитала!
<code>На текущий момент бот по сей день проходит проверки и  исправления! Точность бота составляет 92%!</code>
Для получения максимального профита следуйте следующей инструкции:

🟢 1. Пройти регистрацию в букмекерской конторе <a href="{REF_URL}">1WIN</a>
Если не открывается - заходим с включенным VPN (Швеция). В Play Market/App Store полно бесплатных сервисов, например: Vpnify, Planet VPN, Hotspot VPN и так далее!
<code>Без регистрации по промокоду MEMEZONA доступ к сигналам не будет открыт!</code>
🟢 2. Пополнить баланс своего аккаунта.
🟢 3. Перейти в раздел 1win games и выбрать игру 💣'MINES'.
🟢 4. Выставить кол-во ловушек в размере трёх. Это важно!
🟢 5. Запросить сигнал в боте и ставить по сигналам из бота.
🟢 6. При неудачном сигнале советуем удвоить(Х²) ставку что бы полностью перекрыть потерю при следующем сигнале."""
    photo = types.FSInputFile("instruction.jpg")

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer_photo(photo, text, reply_markup=await ClientKeyboard.back_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "get_signal", ChatJoinFilter(), RegisteredFilter(), DepositFilter())
async def get_signal_start_handler(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer("Выберите кол-во мин", reply_markup=await ClientKeyboard.mines_keyboard())
    await state.set_state(GetSignalStates.chosing_mines)

@router.callback_query(F.data == "get_signal_again", ChatJoinFilter(), RegisteredFilter(), DepositFilter())
async def get_signal_start_handler(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    pth = data['pth']

    try:
        await callback.message.delete()
    except:
        pass
    photo = choice(os.listdir(f"./other/photos/{pth}"))
    number = randint(13425, 124345)
    text = f"""
💣 Игра №{number}
🕓 {str(datetime.datetime.now().date()).replace("-", " ")} {":".join(str(datetime.datetime.now().time()).split(":")[:2])}

Шанс - {round(uniform(91.0, 98.0),2)}%
"""
    await asyncio.sleep(uniform(0.1, 1.1))
    msg = await callback.message.answer("🌐Анализирую базу данных")
    await asyncio.sleep(uniform(0.1, 1.1))
    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=msg.message_id, text="📶Получаю данные с сервера")
    await asyncio.sleep(uniform(0.1, 1.1))
    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=msg.message_id, text="⚠️Изучаю запросы")
    await asyncio.sleep(uniform(0.1, 1.1))
    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=msg.message_id, text="⚠️Формирую ответ")
    await asyncio.sleep(uniform(0.1, 1.1))
    try:
        await bot.delete_message(chat_id=callback.from_user.id, message_id=msg.message_id)
    except:
        pass

    print(photo)
    await callback.message.answer_photo(photo=types.FSInputFile(f"./other/photos/{pth}/{photo}"),
                                        caption=text, reply_markup=await ClientKeyboard.get_signal_keyboard())

@router.callback_query(F.data == "get_signal")
async def get_signal_start_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Пожалуйста, зарегистрируйтесь сначала.", reply_markup=await ClientKeyboard.register_keyboard())
    await state.set_state(RegisterState.input_id)

@router.callback_query(F.data == "get_signal", ChatJoinFilter(), RegisteredFilter())
async def get_signal_start_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Ожидайте подтверждения депозита от 1win.")

@router.callback_query(F.data.in_(["one", "three", "five", "sever"]), ChatJoinFilter(), RegisteredFilter(), DepositFilter())
async def get_signal_finaly(callback: types.CallbackQuery, state: FSMContext):
    print(callback.data)
    if callback.data == "one":
        pth = 1
    elif callback.data == "three":
        pth = 3
    elif callback.data == "five":
        pth = 5
    elif callback.data == "sever":
        pth = 7

    await state.update_data(pth=pth)

    photo = choice(os.listdir(f"./other/photos/{pth}"))
    number = randint(13425, 124345)
    text = f"""
💣 Игра №{number}
🕓 {str(datetime.datetime.now().date()).replace("-", " ")} {":".join(str(datetime.datetime.now().time()).split(":")[:2])}

Шанс - {round(uniform(91.0, 98.0),2)}%
"""
    await asyncio.sleep(uniform(0.1, 1.1))
    await callback.message.edit_text("🌐Анализирую базу данных")
    await asyncio.sleep(uniform(0.1, 1.1))
    await callback.message.edit_text("📶Получаю данные с сервера")
    await asyncio.sleep(uniform(0.1, 1.1))
    await callback.message.edit_text("⚠️Изучаю запросы")
    await asyncio.sleep(uniform(0.1, 1.1))
    await callback.message.edit_text("⚠️Формирую ответ")
    await asyncio.sleep(uniform(0.1, 1.1))
    try:
        await callback.message.delete()
    except:
        pass

    print(photo)
    await callback.message.answer_photo(photo=types.FSInputFile(f"./other/photos/{pth}/{photo}"),
                                        caption=text, reply_markup=await ClientKeyboard.get_signal_keyboard())