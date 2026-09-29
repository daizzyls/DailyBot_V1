# saver.py
import asyncio

from congratulations import congratulations as congrat
from datebase import datebase as database


def save_date():
    with open("datebase.py", "w", encoding="utf-8") as data:
        data.write(f"datebase: dict[int, dict[tuple[str, str], tuple[str, str]]] = {repr(database)}")

async def async_save_date():
    await asyncio.to_thread(save_date)

def save_congratulations():
    with open("congratulations.py", "w", encoding="utf-8") as prize:
        prize.write("congratulations = " + repr(congrat) + "\n")

async def async_save_congratulations():
    await asyncio.to_thread(save_congratulations)