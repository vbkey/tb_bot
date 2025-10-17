from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Профиль"), KeyboardButton(text="Помощь")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
admin_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Админ меню")],
        [KeyboardButton(text="Профиль"),KeyboardButton(text="Помощь")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Пользователи", callback_data="show_users"),
            InlineKeyboardButton(text="Поиск", callback_data="search_user")
        ]
    ]
)
def get_user_manipulate_menu(user_id):
    user_manipulate_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Блокировать", callback_data=f"block_user:{user_id}"),
                InlineKeyboardButton(text="Разлокировать", callback_data=f"unblock_user:{user_id}")
            ]
        ]
    )
    return user_manipulate_menu
profile_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Изменить", callback_data="edit_profile")]
    ]
)