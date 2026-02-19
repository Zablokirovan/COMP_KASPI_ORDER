import asyncio
import telegram


messages, id_employee = telegram.messages_in_telebot()


if __name__ == "__main__":
    asyncio.run(telegram.messages_in_telebot())