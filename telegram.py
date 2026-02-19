import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()


async def main():
    bot = Bot(token= os.getenv('TELEGRAM_BOT_TOKEN'))
    dp = Dispatcher()

    @dp.message(F.text)
    async def handle_text(message: Message):
        user_id = message.from_user.id
        text = message.text

        # --- обработка ---
        if text.isdigit():   # пример обработки
            print(text)
        else:
            await message.answer(f"Вы ввели не коректные даныне")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
