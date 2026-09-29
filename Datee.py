
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from BirthBot import async_save_date
from configur import ADMIN as AD
from datebase import datebase as dt

database = dt
router = Router()
ADMIN = AD


@router.message(Command("date"))
async def write_dates(message: Message):
    id_chat = message.chat.id

    if not message.text:
        await message.answer(
            text="Введите пожалуйста команду текстом. Пример: /date Иван Петров 11-09-2001 или /date Иван - 11-09-2001", 
            parse_mode="HTML"
        )
        return
        
    text_arr = message.text.strip().split(maxsplit=3)

    if len(text_arr) < 4:
        await message.answer(
            "<b>Неверный формат!</b>\n"
            "Используйте: <code>/date Имя Фамилия ДД-ММ-ГГГГ</code>\n"
            "<i>Если фамилии нет, поставьте прочерк: /date Иван - 15-08-1995</i>",
            parse_mode="HTML"
        )
        return
    
    name = text_arr[1]
    raw_surname = text_arr[2]
    raw_date = text_arr[3]

    # Если вместо фамилии ввели прочерк "-", сохраняем пустую строку
    surname = "" if raw_surname in "-/.,\\;:-*/!@#$%&()*-_~`" else raw_surname

    try:
        parsed_date = datetime.strptime(raw_date, "%d-%m-%Y") 
        str_date = parsed_date.strftime("%d-%m")
        str_year = parsed_date.strftime("%Y")
    except ValueError:
        await message.answer(
            "<b>Ошибка в формате даты!</b>\n"
            "Убедитесь, что дата введена как <code>ДД-ММ-ГГГГ</code> (например: 15-08-1995).",
            parse_mode="HTML"
        )
        return

    if id_chat not in database:
        database[id_chat] = {}

    # Сохраняем с кортежем в качестве ключа
    database[id_chat][(name, surname)] = (str_date, str_year)
    await async_save_date()

    # Формируем красивый вывод: если есть фамилия — пишем, иначе только имя
    if surname:
        person_info = f"<b>Имя:</b> {name}\n<b>Фамилия:</b> {surname}"
    else:
        person_info = f"<b>Имя:</b> {name}"

    await message.answer(
        f"Успешно добавлено!\n"
        f"{person_info}\n"
        f"<b>Дата рождения:</b> {str_date}-{str_year}",
        parse_mode="HTML"
    )
    

