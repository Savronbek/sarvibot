import logging
from aiogram import Bot, Dispatcher, types
from config import TOKEN, BOT_NICKNAME
import markups as nav
from aiogram.filters import Command
from aiogram.dispatcher.router import Router
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from db import Database

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)
db = Database('database.db')

# Команда /start
@router.message(Command('start'))
async def cmd_start(message: types.Message):
    if message.chat.type == 'private':
        start_command = message.text.strip()
        referrer_id = start_command[7:] if len(start_command) > 7 else None
        
        if not db.user_exists(message.from_user.id):
            if referrer_id and referrer_id != str(message.from_user.id):
                if db.add_user(message.from_user.id, referrer_id):
                    try:
                        await bot.send_message(referrer_id, "Sizning linkingiz orqali yangi foydalanuvchi qo'shildi!\nTabriklaymiz, siz 1 ballga ega bo'ldingiz!")
                    except Exception as e:
                        logging.error(f"Ошибка при отправке сообщения рефереру: {e}")
                else:
                    await bot.send_message(message.from_user.id, "Произошла ошибка при регистрации пользователя.")
            elif referrer_id == str(message.from_user.id):
                await bot.send_message(message.from_user.id, "Нельзя регистрироваться по собственной реферальной ссылке")
            else:
                if db.add_user(message.from_user.id):
                    await bot.send_message(message.from_user.id, 'Assalomu aleykum!\nXush kelibsiz!', reply_markup=nav.mainMenu)
                else:
                    await bot.send_message(message.from_user.id, "Произошла ошибка при регистрации пользователя.")
        else:
            await bot.send_message(message.from_user.id, 'Xush kelibsiz!', reply_markup=nav.mainMenu)

# Обработка сообщения "профиль"
@router.message()
async def bot_message(message: types.Message):
    if message.text == 'Profil':
        referral_count = db.count_referrals(message.from_user.id)
        await bot.send_message(message.from_user.id, f"ID: {message.from_user.id}\nhttps://t.me/{BOT_NICKNAME}?start={message.from_user.id}\nTo'plangan ballar soni: {referral_count}")

# Асинхронная функция запуска бота
async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
