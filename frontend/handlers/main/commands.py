from aiogram.types import Message
from loader import dp
from text.keyboard import search_kb


@dp.message_handler(commands=["start", "help"], state="*")
async def send_welcome(message: Message):
    print(message.from_user.locale.language)
    if message.from_user.locale.language == "ru":
        await message.reply("Привет! Я помогу тебе узнать некоторую информацию о странах и городах",
                            reply_markup=search_kb["ru"])
    else:
        await message.reply("Hello! I'm Countries Informator Bot", reply_markup=search_kb["en"])
