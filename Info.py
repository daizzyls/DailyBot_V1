
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

# Импортируем из config, а не из BirthBot!
from configur import ADMIN as AD
from datebase import datebase as dt

database = dt
router = Router()
ADMIN = AD

@router.message(Command("info"))
async def get_info(message: Message):
    chat_id = message.chat.id
    chat_type = message.chat.type  # 'private', 'group', 'supergroup'
    if message.from_user:
        user_id = str(message.from_user.id)
    else:
        user_id = "0"
        
    is_admin = (user_id == ADMIN)
    result_text = ""
    
        # ВАРИАНТ 1: Администратор бота — выводим абсолютно все записи из всех чатов
    if is_admin:
        count = 0
        
        # Заголовок таблицы
        table_body = f"| {'Surname':<12} | {'Name':<12} | {'Birth_Date':<10} |\n"
        table_body += f"|{'-'*14}|{'-'*14}|{'-'*12}|\n"

        for _, members in database.items():
            for (name, surname), (date, year) in members.items():
                count += 1
                full_surname = surname if surname else "None"
                full_date = f"{date}-{year}"
                
                # Обрезаем длинные имена, чтобы таблица не разъезжалась на экранах телефонов
                s_print = (full_surname[:11] + "…") if len(full_surname) > 12 else full_surname
                n_print = (name[:11] + "…") if len(name) > 12 else name

                # Двоеточие пишется ВНУТРИ фигурных скобок: {переменная:<ширина}
                table_body += f"| {s_print:<12} | {n_print:<12} | {full_date:<10} |\n"

        if count == 0:
            await message.answer("База данных абсолютно пуста.")
            return

        # Оборачиваем таблицу в <pre>, чтобы включить моноширинный шрифт
        result_text = f"<b>[ADMIN] Full List of BirthDates:</b>\n<pre>{table_body}</pre>"

        # Отправляем сообщение
        if len(result_text) > 4000:
            for x in range(0, len(result_text), 4000):
                await message.answer(result_text[x:x+4000], parse_mode="HTML")
        else:
            await message.answer(text=result_text, parse_mode="HTML")
#--------------------------------------------------------------------------------------------------------
    elif chat_type in ['group', 'supergroup']: 
        if chat_id not in database or not database[chat_id]:
            await message.answer(text="Current list is empty. :(\n")
            return

        table_body = f"| {'Surname':<12} | {'Name':<12} | {'Birth_Date':<10} |\n"
        table_body += f"|{'-'*14}|{'-'*14}|{'-'*12}|\n"

        for (name, surname), (date, year) in database[chat_id].items():
            full_surname = surname if surname else "None"
            full_date = f"{date}-{year}"
            
            s_print = (full_surname[:11] + "…") if len(full_surname) > 12 else full_surname
            n_print = (name[:11] + "…") if len(name) > 12 else name

            table_body += f"| {s_print:<12} | {n_print:<12} | {full_date:<10} |\n"

        result_text = f"<b>Group List of BirthDates:</b>\n<pre>{table_body}</pre>"
    
        # ВАРИАНТ 3: Личные сообщения
    elif chat_type == 'private':
        if chat_id not in database or not database[chat_id]:
            await message.answer(text="Your list is empty. :(\n")
            return

        table_body = f"| {'Surname':<12} | {'Name':<12} | {'Birth_Date':<10} |\n"
        table_body += f"|{'-'*14}|{'-'*14}|{'-'*12}|\n"

        for (name, surname), (date, year) in database[chat_id].items():
            full_surname = surname if surname else "None"
            full_date = f"{date}-{year}"
            
            s_print = (full_surname[:11] + "…") if len(full_surname) > 12 else full_surname
            n_print = (name[:11] + "…") if len(name) > 12 else name

            table_body += f"| {s_print:<12} | {n_print:<12} | {full_date:<10} |\n"

        result_text = f"<b>Personal List of BirthDates:</b>\n<pre>{table_body}</pre>"

    # Отправка сформированного результата
    if result_text:
        if len(result_text) > 4000:
            for x in range(0, len(result_text), 4000):
                await message.answer(result_text[x:x+4000], parse_mode="HTML")
        else:
            await message.answer(text=result_text, parse_mode="HTML")