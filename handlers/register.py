from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db.database import get_staff, add_staff

class StaffRegister(StatesGroup):
    telefon = State()
    ism = State()
    rol = State()

def telefon_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True))
    return kb

async def start(message: Message, state: FSMContext):
    await state.finish()
    staff = await get_staff(message.from_user.id)
    if staff:
        await message.answer(
            f"Xush kelibsiz, {staff[2]}! 👋\nRolingiz: {staff[4]}",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            "LimonFood Admin botga xush kelibsiz!\n\nTelefon raqamingizni yuboring:",
            reply_markup=telefon_keyboard()
        )
        await StaffRegister.telefon.set()

async def get_telefon(message: Message, state: FSMContext):
    if not message.contact:
        await message.answer("Iltimos tugmani bosing 👇", reply_markup=telefon_keyboard())
        return
    await state.update_data(telefon=message.contact.phone_number)
    await message.answer("Ismingizni kiriting:", reply_markup=ReplyKeyboardRemove())
    await StaffRegister.ism.set()

async def get_ism(message: Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await message.answer(
        "Rolingizni tanlang:",
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
            KeyboardButton("🏪 Restoran"),
            KeyboardButton("🛵 Kuryer"),
            KeyboardButton("👑 Admin")
        )
    )
    await StaffRegister.rol.set()

async def get_rol(message: Message, state: FSMContext):
    if message.text not in ["🏪 Restoran", "🛵 Kuryer", "👑 Admin"]:
        await message.answer("Iltimos tugmadan tanlang!")
        return
    data = await state.get_data()
    rol_map = {"🏪 Restoran": "restoran", "🛵 Kuryer": "kuryer", "👑 Admin": "admin"}
    rol = rol_map[message.text]
    await add_staff(message.from_user.id, data["ism"], data["telefon"], rol)
    await state.finish()
    await message.answer(
        f"✅ Ro'yxatdan o'tdingiz!\nAdmin tasdiqlashini kuting...",
        reply_markup=ReplyKeyboardRemove()
    )

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_message_handler(get_telefon, content_types=["contact"], state=StaffRegister.telefon)
    dp.register_message_handler(get_ism, state=StaffRegister.ism)
    dp.register_message_handler(get_rol, state=StaffRegister.rol)
