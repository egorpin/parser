from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

notification_interval = ReplyKeyboardRemove(keyboard=[[KeyboardButton(text='1 час')],
                                                       [KeyboardButton(text='3 часа')],
                                                       [KeyboardButton(text='6 часов')],
                                                       [KeyboardButton(text='12 часов')],
                                                       [KeyboardButton(text='Раз в день')],
                                                       [KeyboardButton(text='Никогда')]], resize_keyboard=True)


taglist = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Программирование", callback_data='programming')],
                                                [InlineKeyboardButton(text="Сайты", callback_data='websites')],
                                                [InlineKeyboardButton(text="Дизайн", callback_data='design')],
                                                [InlineKeyboardButton(text="Тексты", callback_data='texts')],
                                                [InlineKeyboardButton(text="Достаточно", callback_data='cancel')]])
