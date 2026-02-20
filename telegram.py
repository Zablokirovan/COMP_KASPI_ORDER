import asyncio
import os
import database
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()


async def messages_in_telebot():
    bot = Bot(token= os.getenv('TELEGRAM_BOT_TOKEN'))
    dp = Dispatcher()

    @dp.message(F.text)
    async def handle_text(message: Message):
        user_id = message.from_user.id
        text = message.text

        result_database = database.get_info_in_db(user_id)
        if result_database[1]:
            if result_database[0] == 'WAIT_ORDER':
                if len(text) >= 6 and str.isdigit(text):
                    await message.answer("Валидный код")
                else:
                    await message.answer("Введен не верный код")



        else:
            database.insert_first_data(user_id)
            await message.answer("📝Введите номер заказа Kaspi")



    await dp.start_polling(bot)


#await message.answer(f"Вы ввели не коректные даныне")


if __name__ == "__main__":
    asyncio.run(messages_in_telebot())