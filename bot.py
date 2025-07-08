import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from config import API_TOKEN
from database import init_db
from handlers import start

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def handle_start(msg: Message):
    await start(msg)

def main():
    init_db()
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()