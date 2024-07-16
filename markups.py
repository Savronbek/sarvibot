from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnProfile = KeyboardButton(text="Profil")

mainMenu = ReplyKeyboardMarkup(keyboard=[[btnProfile]], resize_keyboard=True)