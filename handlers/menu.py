from aiogram import Dispatcher
from aiogram.types import Message

async def stub(message: Message):
    await message.answer("Tez kunda...")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(stub, text="test")
