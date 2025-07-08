from aiogram import types
from database import init_db

async def start(message: types.Message):
    await message.answer("Welcome to the Crypto Shop Bot! Use /shop to begin.")

# Placeholder: Add more handlers for browsing cities, products, top-up, etc.