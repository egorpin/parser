from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

import app.config as config

default = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Изменить настройки')]], resize_keyboard=True)

notification_interval = ReplyKeyboardRemove(keyboard=[[KeyboardButton(text='1 час')],
                                                      [KeyboardButton(text='3 часа')],
                                                      [KeyboardButton(text='6 часов')],
                                                      [KeyboardButton(text='12 часов')],
                                                      [KeyboardButton(text='Раз в день')],
                                                      [KeyboardButton(text='Никогда')]], resize_keyboard=True)

initial_buttons = {tag:tag for tag in config.categories}
initial_buttons['Достаточно'] = 'cancel'

def make_taglist(*exclude_tags):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=tag, callback_data=callback)] for tag, callback in initial_buttons.items() if tag not in exclude_tags])