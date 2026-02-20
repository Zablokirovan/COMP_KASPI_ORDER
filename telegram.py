import asyncio
import os
import aiohttp
import database
import kaspi
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

async def messages_in_telebot():
    await database.init_db()

    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    dp = Dispatcher()

    timeout = aiohttp.ClientTimeout(total=8, connect=3, sock_read=30)

    async with aiohttp.ClientSession(timeout=timeout) as session:

        @dp.message(F.text)
        async def handle_text(message: Message):
            user_id = message.from_user.id
            text = message.text

            state, found = await database.get_info_in_db(user_id)

            if found:

                if state == "WAIT_ORDER":

                    if len(text) >= 6 and text.isdigit():

                        order_data = await kaspi.get_info_for_order(session, text)

                        data = order_data['data'][0]['attributes']

                        await message.answer(f"<b>Информация о заказе</b>: {data['code']}\n"
                                             f"<b>Имя клиента</b>: {data['customer']['name']+' '+data['customer']['lastName']}\n"
                                             f"<b>Телефон клиента</b>: {data['customer']['cellPhone']}\n"
                                             f"<b>Адрес доставки</b>: {data['deliveryAddress']['formattedAddress']}\n", parse_mode='HTML')

                        await kaspi.sending_code(order_data['data'][0]['id'],text, session)
                    else:
                        await message.answer("Введен не верный код")
            else:
                await database.insert_first_data(user_id)
                await message.answer("📝Введите номер заказа Kaspi")

        try:
            await dp.start_polling(bot)   # ✅ ВНУТРИ async with session
        finally:
            await database.close_db()

if __name__ == "__main__":
    asyncio.run(messages_in_telebot())