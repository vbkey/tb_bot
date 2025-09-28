import asyncio
from config import *
from tinydb import TinyDB, Query
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
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

class ProfileEdit(StatesGroup):
    name = State()

async def get_profile(user_id):
    User = Query()
    profile = await asyncio.to_thread(users_table.search, User.user_id == user_id)
    return profile

async def add_profile(name, user_id):
    await asyncio.to_thread(users_table.insert, {"name": name, "user_id": user_id})

async def save_profile(name, user_id):
    User = Query()
    await asyncio.to_thread(users_table.update, {"name": name}, User.user_id == user_id)

menu_btns = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Профиль"), KeyboardButton(text="Помощь")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

admin_menu_btns = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Админ меню")],
        [KeyboardButton(text="Профиль"),KeyboardButton(text="Помощь")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

profile_btns = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Изменить", callback_data="edit_profile")]
    ]
)

async def check_admin(admin_id):
    admin = Query()
    data = await asyncio.to_thread(admins_table.search, admin.admin_id == admin_id)
    if data:
        return True
    return False
# --- Хэндлеры ---
@router.message(Command("start"))
async def start_command(message: Message):
    is_admin = await check_admin(message.from_user.id)
    if is_admin:
        await message.answer("Заготовка бота", reply_markup=admin_menu_btns)
    else:
        await message.answer("Заготовка бота", reply_markup=menu_btns)
    
@router.message(F.text == "Админ меню") 
async def echo(message: Message):
    is_admin = await check_admin(message.from_user.id)
    if is_admin:
        await message.answer("Админ меню")
    
@router.message(F.text == "Профиль") 
async def echo(message: Message, state: FSMContext):
    profile = await get_profile(message.from_user.id)
    if not profile: 
        await message.answer("Задайте никнейм:")
        await state.set_state(ProfileForm.name)
    else:
        await message.answer(f"Никнейм: {profile[0]["name"]}\nКонец!", reply_markup=profile_btns)

@router.callback_query(F.data == "edit_profile")
async def echo(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Задайте никнейм:")
    await state.set_state(ProfileEdit.name)
    await callback.answer()

@router.message(ProfileEdit.name) 
async def echo(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    user_data = await state.get_data()
    await save_profile(user_data["name"], message.from_user.id)
    await message.answer('Данные сохраненны!')
    await state.clear()

@router.message(ProfileForm.name) 
async def echo(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    user_data = await state.get_data()
    await add_profile(user_data["name"], message.from_user.id)
    await message.answer('Данные сохраненны!')
    await state.clear()

@router.message(F.text == "Помощь") 
async def echo(message: Message):
    await message.answer("Помощь")

# --- Запуск ---
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
