import asyncio
from config import *
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command  # <-- новый фильтр


bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

menu_btns = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Профиль")],
        [KeyboardButton(text="Помощь"), KeyboardButton(text="Админ меню")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# --- Хэндлеры ---
@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Заготовка бота", reply_markup=menu_btns)
@router.message(F.text == "Админ меню") 
async def echo(message: Message):
    await message.answer("Админ меню")
@router.message(F.text == "Профиль") 
async def echo(message: Message):
    await message.answer("Профиль")
@router.message(F.text == "Помощь") 
async def echo(message: Message):
    await message.answer("Помощь")

# --- Запуск ---
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
