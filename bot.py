import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from config import API_TOKEN
from database import init_db
from handlers import start, shop, city_callback, product_callback, option_callback, ShopFlow

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=["start"])
async def handle_start(msg: Message):
    await start(msg)

@dp.message_handler(commands=["shop"])
async def handle_shop(msg: Message):
    await shop(msg, dp.current_state(user=msg.from_user.id))

@dp.callback_query_handler(lambda c: c.data.startswith("city_"), state=ShopFlow.ChoosingCity)
async def handle_city(call, state):
    await city_callback(call, state)

@dp.callback_query_handler(lambda c: c.data.startswith("product_"), state=ShopFlow.ChoosingProduct)
async def handle_product(call, state):
    await product_callback(call, state)

@dp.callback_query_handler(lambda c: c.data.startswith("option_"), state=ShopFlow.ChoosingAmount)
async def handle_option(call, state):
    await option_callback(call, state)

def main():
    init_db()
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()