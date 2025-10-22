import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import BaseMiddleware
from Markups import *
from DbHelper import *
from config import *

#Creating bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

#States
class ProfileEdit(StatesGroup):
    name = State()
class Admin_functions(StatesGroup):
    block_user = State()

#Middlewares
class BlockCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            if await check_block(event.from_user.id):
                await event.answer("Пошли нахуй. Пожалуйста")
                return
        return await handler(event, data)
class ProfileCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        state: FSMContext = data["state"]
        if isinstance(event, Message):
            profile = await get_profile(event.from_user.id)
            if not profile:
                await add_profile(event.from_user.username, event.from_user.id)
        return await handler(event, data)
dp.message.middleware(BlockCheckMiddleware())
dp.message.middleware(ProfileCheckMiddleware())

#Routes
@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    is_admin = await check_admin(message.from_user.id)
    if is_admin:
        await message.answer("Заготовка бота", reply_markup=admin_main_menu)
    else:
        await message.answer("Заготовка бота", reply_markup=main_menu)
@router.message(F.text == "Админ меню") 
async def echo(message: Message):
    is_admin = await check_admin(message.from_user.id)
    if is_admin:
        await message.answer("Используйте с умом Мистер Админ!", reply_markup=admin_menu)
@router.callback_query(F.data == "show_users")
async def echo(callback: CallbackQuery):
    users = await get_users()
    for user in users:
        markup = await get_user_manipulate_menu(user["user_id"])
        await callback.message.answer(f'Имя: {user["name"]} ID: {user["user_id"]}', reply_markup=markup)
    await callback.answer()
@router.callback_query(F.data.startswith("block_user:"))
async def echo(callback: CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    await block_user(user_id)
    new_markup = await get_user_manipulate_menu(user_id)
    await callback.message.edit_reply_markup(reply_markup=new_markup)
    await callback.answer()
@router.callback_query(F.data.startswith("unblock_user:"))
async def echo(callback: CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    await unblock_user(user_id)
    new_markup = await get_user_manipulate_menu(user_id)
    await callback.message.edit_reply_markup(reply_markup=new_markup)
    await callback.answer()
@router.callback_query(F.data.startswith("give_admin:"))
async def echo(callback: CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    await give_admin(user_id)
    new_markup = await get_user_manipulate_menu(user_id)
    await callback.message.edit_reply_markup(reply_markup=new_markup)
    await callback.answer()
@router.message(F.text == "Профиль") 
async def echo(message: Message):
    profile = await get_profile(message.from_user.id)
    await message.answer(f"Никнейм: {profile[0]["name"]}\nКонец!", reply_markup=profile_menu)
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
@router.message(F.text == "Помощь") 
async def echo(message: Message):
    await message.answer("Помощь")

#Running bot
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
