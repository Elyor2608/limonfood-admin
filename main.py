import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers import register, menu

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

register.register_handlers(dp)
menu.register_handlers(dp)

async def on_startup(dp):
    print("LimonFood Admin bot ishga tushdi! 🚀")

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
