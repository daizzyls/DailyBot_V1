# =========================IMPORT========================= #
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from congratulations import congratulations
from datebase import datebase
from Datee import router as date_router
from Gift import router as gift_router
from Info import router as info_router
from strTOK import BOT_TOKEN

# 1. Импортируем фоновые задачи из вашего файла tasks.py
from tasks import clear_daily_list, daily_date
from today import congratulated_today

# =========================SETTINGS========================= #
TELEGRAM_TOKEN = BOT_TOKEN
ADMIN = '1054191711'

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Регистрация роутеров
dp.include_router(date_router)
dp.include_router(info_router)
dp.include_router(gift_router)

# =========================DataBase========================= #
database = datebase
congrat = congratulations
today_congratulated = congratulated_today

# =========================Keyboard========================= #
info_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/info")]  # Используем команду /info для кликабельности
    ],
    resize_keyboard=True
)

# =========================FUNCTIONS========================= #
@dp.message(CommandStart())
async def strart_instruction(message: Message):
    await message.answer(
        text="<b>Hi! I'm DailyBot.</b>\n"
             "<b>Here are my commands:</b>\n\n"
             "<code>/date</code> - <b>add your name and birthdate to database</b>\n"
             "<blockquote><b>Example: <i>/date Name DD-MM-YYYY</i></b></blockquote>\n\n"
             "<code>/gift</code> - <b>add your congratulation to database</b>\n"
             "<blockquote><b>Example: <i>/gift your_text</i></b></blockquote>\n"
             "<b>If you need to enter name in text , write like this <code>{name}</code></b>\n"
             "<blockquote><b>Example: <i>/gift Поздравляю тебя {name}!</i></b></blockquote>\n\n"
             "<code>/info</code> - <b>send database in this chat</b>",
        parse_mode="HTML",
        reply_markup=info_keyboard
    )


# ------------------save-functions---------------------------------------
def save_date():
    with open("datebase.py", "w", encoding="utf-8") as data:
        data.write(f"datebase = {database}")


async def async_save_date():
    await asyncio.to_thread(save_date)


def save_congratulations():
    with open("congratulations.py", "w", encoding="utf-8") as prize:
        prize.write("congratulations = " + repr(congrat) + "\n")


async def async_save_congratulations():
    await asyncio.to_thread(save_congratulations)


# =========================LAUNCH========================= #
async def main():
    # 2. Передаем 'bot' внутрь daily_date
    asyncio.create_task(daily_date(bot))
    asyncio.create_task(clear_daily_list())

    print("Bot is RUN....")
    print(database)

    # Очищаем очередь накопившихся сообщений
    await bot.delete_webhook(drop_pending_updates=True)
    
    # 3. Чистый запуск поллинга
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())