import asyncio
import random
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from aiogram import Bot

from congratulations import congratulations as congrat
from datebase import datebase as database
from today import congratulated_today as today_congratulated


# 1. Добавляем параметр bot: Bot в аргументы функции
async def daily_date(bot: Bot):
    while True:
        tz_moscow = ZoneInfo("Europe/Moscow")
        now = datetime.now(tz=tz_moscow)
        current_date = now.strftime("%d-%m")
        current_year = now.strftime("%Y")
        
        for chat_idd, member in database.items():
            for (name, surname), (date, year) in member.items():
                
                full_name = f"{name} {surname}".strip() if surname and surname != "-" else name
                
                if current_date == date and full_name not in today_congratulated:
                    how_many_years = int(current_year) - int(year)
                    template = random.choice(congrat) + f"\nХОУ ХОУ ХОУ! \nТебе исполнилось: {how_many_years}"
                    
                    try:
                        congratulation_text = template.format(name=full_name) 
                    except KeyError:
                        congratulation_text = template
                    
                    try:
                        # Теперь объект bot доступен из аргументов
                        await bot.send_message(
                            chat_id=chat_idd,
                            text=congratulation_text
                        )
                        today_congratulated.append(full_name)
                    except Exception as e:
                        print(f"Ошибка отправки в чат {chat_idd}: {e}")
                        
        # Проверяем раз в 1 час (3600 сек) вместо 60 сек, чтобы снизить нагрузку
        await asyncio.sleep(3600)


async def clear_daily_list():
    tz_moscow = ZoneInfo("Europe/Moscow")

    while True:
        now = datetime.now(tz=tz_moscow)
        tomorrow = now.date() + timedelta(days=1)
        midnight = datetime.combine(
            tomorrow, datetime.min.time(), tzinfo=tz_moscow
        )
        seconds_until_midnight = (midnight - now).total_seconds()

        await asyncio.sleep(seconds_until_midnight)

        today_congratulated.clear()
        print(f"[{datetime.now(tz=tz_moscow)}] Список today_congratulated успешно очищен!")