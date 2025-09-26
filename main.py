import asyncio
from config import *
from tinydb import TinyDB, Query
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

db = TinyDB("db.json")
users_table = db.table('users')
admins_table = db.table('admins')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

class ProfileForm(StatesGroup):
    name = State()

async def save_profile(name, user_id):
    users_table.insert({"name": name, "user_id": user_id})

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
async def echo(message: Message, state: FSMContext):
    await message.answer("Задайте никнейм:")
    await state.set_state(ProfileForm.name)

@router.message(ProfileForm.name) 
async def echo(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    user_data = await state.get_data()
    await save_profile(user_data["name"], message.from_user.id)
    await message.answer('Данные сохраненны!')

@router.message(F.text == "Помощь") 
async def echo(message: Message):
    await message.answer("Помощь")

# --- Запуск ---
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
