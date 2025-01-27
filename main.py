import os
import logging
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from db import Database
import markups as nav
import asyncio
from aiogram.filters import Command

# Загрузка переменных окружения
load_dotenv()

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
db = Database('database.db')

# Команда /start
@dp.message(Command('start'))
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
@dp.message()
async def bot_message(message: types.Message):
    if message.text == 'Profil':
        referral_count = db.count_referrals(message.from_user.id)
        await bot.send_message(message.from_user.id, f"ID: {message.from_user.id}\nhttps://t.me/{os.getenv('BOT_NICKNAME')}?start={message.from_user.id}\nTo'plangan ballar soni: {referral_count}")

# Запуск бота
async def main():
    # Удаляем вебхук, если он был установлен
    await bot.delete_webhook(drop_pending_updates=True)
    # Запускаем polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
