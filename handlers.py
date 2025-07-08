from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3

class ShopFlow(StatesGroup):
    ChoosingCity = State()
    ChoosingProduct = State()
    ChoosingAmount = State()

async def start(message: types.Message):
    await message.answer("Welcome to the Crypto Shop Bot! Use /shop to begin.")

async def shop(message: types.Message, state: FSMContext):
    conn = sqlite3.connect("shop.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM cities")
    cities = cur.fetchall()
    keyboard = InlineKeyboardMarkup()
    for cid, name in cities:
        keyboard.add(InlineKeyboardButton(name, callback_data=f"city_{cid}"))
    await message.answer("Choose your city:", reply_markup=keyboard)
    await ShopFlow.ChoosingCity.set()

async def city_callback(call: types.CallbackQuery, state: FSMContext):
    city_id = int(call.data.split("_")[1])
    await state.update_data(city_id=city_id)
    conn = sqlite3.connect("shop.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM products WHERE city_id = ?", (city_id,))
    products = cur.fetchall()
    keyboard = InlineKeyboardMarkup()
    for pid, name in products:
        keyboard.add(InlineKeyboardButton(name, callback_data=f"product_{pid}"))
    await call.message.edit_text("Select a product:", reply_markup=keyboard)
    await ShopFlow.ChoosingProduct.set()

async def product_callback(call: types.CallbackQuery, state: FSMContext):
    product_id = int(call.data.split("_")[1])
    await state.update_data(product_id=product_id)
    conn = sqlite3.connect("shop.db")
    cur = conn.cursor()
    cur.execute("SELECT id, amount, price FROM product_options WHERE product_id = ?", (product_id,))
    options = cur.fetchall()
    keyboard = InlineKeyboardMarkup()
    for oid, amount, price in options:
        keyboard.add(InlineKeyboardButton(f"{amount} - ${price}", callback_data=f"option_{oid}"))
    await call.message.edit_text("Choose amount:", reply_markup=keyboard)
    await ShopFlow.ChoosingAmount.set()

async def option_callback(call: types.CallbackQuery, state: FSMContext):
    option_id = int(call.data.split("_")[1])
    user_id = call.from_user.id
    conn = sqlite3.connect("shop.db")
    cur = conn.cursor()
    cur.execute("SELECT price FROM product_options WHERE id = ?", (option_id,))
    price = cur.fetchone()[0]
    cur.execute("SELECT balance FROM users WHERE telegram_id = ?", (user_id,))
    row = cur.fetchone()
    if row and row[0] >= price:
        new_balance = row[0] - price
        cur.execute("UPDATE users SET balance = ? WHERE telegram_id = ?", (new_balance, user_id))
        cur.execute("INSERT INTO orders(user_id, option_id, status) VALUES((SELECT id FROM users WHERE telegram_id = ?), ?, 'paid')", (user_id, option_id))
        conn.commit()
        await call.message.answer("✅ Payment successful!\n\n📦 Product Details:\nLocation: Your city’s delivery point\nPickup: 24/7 terminal\nSupport: @supportusername")
    else:
        await call.message.answer("❌ Insufficient balance. Please top up via /topup")
    await state.finish()
