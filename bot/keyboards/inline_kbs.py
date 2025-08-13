from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

prev_button = InlineKeyboardButton(text="<<", callback_data="prev")
next_button = InlineKeyboardButton(text=">>", callback_data="next")

def counter_button(number: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=str(number), callback_data=" ")

def get_meanings_kb(number: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[prev_button, counter_button(number), next_button]])
