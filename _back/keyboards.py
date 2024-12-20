from aiogram.types import InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.types.web_app_info import WebAppInfo
from aiogram import types
from aiogram.types import BotCommand

start_menu = [
    BotCommand(command='start', description='PLAY'),
]


# bot_menu_button =
# url = "https://printy.top/telegram.html"
# url = 'https://192.168.0.100:443'
# url = 'https://dexstudioapp.site'

def get_url(user_id):
    url = f'https://dexstudioapp.site/pussycoin?user_id={user_id}'
    # url = f'https://127.0.0.1:443?user_id={user_id}'

    rows_play_kb = [
        [
            InlineKeyboardButton(text='PLAY', web_app=WebAppInfo(url=url)),
        ],
        [
            InlineKeyboardButton(text='JOIN COMMUNITY', url='https://t.me/+8K1Wfb_o_3NhNjk1'),
        ],
    ]
    play_kb = types.InlineKeyboardMarkup(inline_keyboard=rows_play_kb)
    return play_kb


# def get_urls(user_id):
#     web_app = f'https://127.0.0.1:443?user_id={user_id}'
#     button_webapp = InlineKeyboardButton(text="Open Web App", web_app=web_app)
#     markup = InlineKeyboardMarkup().add(button_webapp)


# def get_urls(user_id):
#     url = f'https://127.0.0.1:443?user_id={user_id}'
#     markkup = (
#         InlineKeyboardBuilder()
#         .button(text="Start App", web_app=WebAppInfo(url=url))
#     ).as_markup()


#--- Start Keyboard ---
# start_kb = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text="PLAY", web_app=WebAppInfo(url=url)),
#         ],
#         # [
#         #     KeyboardButton(text="Instruction"),
#         #     KeyboardButton(text="Subscribe", callback_data="subscribe")
#         # ],
#     ],
#     resize_keyboard=True,
#     # input_field_placeholder='What?'
# )

# --- Delete Keyboard ---

del_kb = ReplyKeyboardRemove()

# --- Subscribe Inline Buttons ---

# sub_kb = [
#     [
#         InlineKeyboardButton(text='1 Day: 100K VND', callback_data='sub1day'),
#     ],
#     [
#         InlineKeyboardButton(text='7 Days: 400K VND', callback_data='sub7days'),
#     ],
#     [
#         InlineKeyboardButton(text='1 Month: 1M VND', callback_data='sub1month'),
#     ],
#     [
#         InlineKeyboardButton(text='FOREVER: 10M VND', callback_data='subForever'),
#     ],
# ]
# sub_keyboard = types.InlineKeyboardMarkup(inline_keyboard=sub_kb)
