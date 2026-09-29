


from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from BirthBot import ADMIN as AD
from BirthBot import async_save_congratulations, congrat
from datebase import datebase as dt

database = dt
router = Router()
ADMIN = AD



@router.message(Command("gift"))
async def gift_writing(message: Message):
    
    if not message.text : #Проверка на существование текста 
        await message.answer(
            text= "Введите пожалуйста команду текстом. Пример: /gift Поздравляю тебя {name}" , 
            parse_mode= "HTML")
        return

    text_arr = message.text.split(maxsplit=1)

    congratulation_text = text_arr[1]

    if len(text_arr) < 2:
            await message.answer(
                "<b>Неверный формат!</b>\n"
                "Используйте: <code>/date Имя ДД-ММ-ГГГГ</code>\n"
                "<i>Пример: /date Name 15-08-1995</i>",
                parse_mode="HTML"
            )
            return

    congratulation_text = text_arr[1]
    
    congrat.append(congratulation_text)
        
        
    await async_save_congratulations()
    
    await message.answer(
            f"<b>Поздравление успешно добавлено!</b>\n\n"
            f"<i>Текст:</i> {congratulation_text}",
            parse_mode="HTML"
        )
