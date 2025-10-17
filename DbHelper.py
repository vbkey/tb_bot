import asyncio
from tinydb import TinyDB, Query

#Creating db
db = TinyDB("db.json")
users_table = db.table('users')
admins_table = db.table('admins')

#Functions
async def check_block(user_id):
    user = Query()
    data = await asyncio.to_thread(users_table.search, user.user_id == user_id)
    if data:
        return data[0]["is_block"]
    else:
        return False
async def check_admin(admin_id):
    admin = Query()
    data = await asyncio.to_thread(admins_table.search, admin.admin_id == admin_id)
    if data:
        return True
    return False
async def get_profile(user_id):
    User = Query()
    profile = await asyncio.to_thread(users_table.search, User.user_id == user_id)
    return profile
async def add_profile(name, user_id):
    await asyncio.to_thread(users_table.insert, {"name": name, "user_id": user_id, "is_block": False})
async def save_profile(name, user_id):
    User = Query()
    await asyncio.to_thread(users_table.update, {"name": name}, User.user_id == user_id)
async def get_users():
    users = await asyncio.to_thread(users_table.all)
    return users
async def block_user(user_id):
    User = Query()
    await asyncio.to_thread(users_table.update, {"is_block": True}, User.user_id == user_id)
async def unblock_user(user_id):
    User = Query()
    await asyncio.to_thread(users_table.update, {"is_block": False}, User.user_id == user_id)