import logging
   import asyncio

   from aiogram import Dispatcher, Bot
   from aiohttp import web

   from config import BOT_TOKEN, ADMIN_ID
   from handlers.client import router as client_router
   from handlers.admin import router as admin_router
   from database.db import DataBase

   logging.basicConfig(level=logging.INFO)

   dp = Dispatcher()
   bot = Bot(BOT_TOKEN)
   dp.include_routers(client_router, admin_router)

   # Хендлер для обработки постбэков от 1win
   async def handle_postback(request):
       data = await request.json()
       logging.info(f"Получен постбэк: {data}")

       # Извлекаем данные из постбэка
       user_id_1win = data.get("user_id")  # ID пользователя на 1win
       event_type = data.get("event_type")  # Тип события (registration, first_deposit)
       amount = data.get("amount", 0)  # Сумма депозита (если есть)

       # Ищем Telegram ID пользователя в базе данных по user_id_1win
       query = "SELECT user_id FROM users WHERE user_id_1win = ?"
       result = await DataBase.con.execute(query, (user_id_1win,))
       telegram_id = await result.fetchone()

       if telegram_id:
           telegram_id = telegram_id[0]
           # Формируем сообщение для админа
           if event_type == "registration":
               message = f"Новая регистрация: {user_id_1win}"
               await DataBase.update_verifed(telegram_id)
               # Уведомляем пользователя
               await bot.send_message(telegram_id, "Ваша регистрация на 1win подтверждена! Пожалуйста, сделайте депозит, чтобы получить доступ к сигналам.")
           elif event_type == "first_deposit":
               message = f"{user_id_1win}: депозит: {amount}"
               await DataBase.update_deposited(telegram_id)
               # Уведомляем пользователя
               await bot.send_message(telegram_id, f"Ваш депозит на сумму {amount} подтверждён! Теперь вы можете получить сигналы.")
           else:
               message = f"Неизвестное событие: {event_type} для пользователя {user_id_1win}"

           # Отправляем уведомление админу
           await bot.send_message(chat_id=ADMIN_ID, text=message)
       else:
           message = f"Пользователь с 1win ID {user_id_1win} не найден в базе данных."
           logging.warning(message)
           await bot.send_message(chat_id=ADMIN_ID, text=message)

       return web.Response(text="OK")

   # Настройка веб-сервера для постбэков
   app = web.Application()
   app.router.add_post("/callback", handle_postback)

   async def on_startup(_):
       await DataBase.on_startup()
       logging.info("Бот запущен")

   async def on_shutdown(_):
       logging.info("Бот останавливается...")
       # Закрываем сессию бота
       await bot.session.close()
       # Закрываем соединение с базой данных
       if DataBase.con:
           await DataBase.con.close()
       logging.info("Бот остановлен")

   async def main():
       # Запускаем веб-сервер для постбэков на порту 8080
       runner = web.AppRunner(app)
       await runner.setup()
       site = web.TCPSite(runner, "0.0.0.0", 8080)
       await site.start()
       logging.info("Веб-сервер для постбэков запущен на порту 8080")

       # Запускаем бота
       try:
           await bot.delete_webhook(drop_pending_updates=True)
           await dp.start_polling(bot)
       except Exception as e:
           logging.error(f"Ошибка при запуске бота: {e}")
           raise
       finally:
           # Останавливаем веб-сервер
           await runner.cleanup()

   if __name__ == "__main__":
       dp.startup.register(on_startup)
       dp.shutdown.register(on_shutdown)
       asyncio.run(main())