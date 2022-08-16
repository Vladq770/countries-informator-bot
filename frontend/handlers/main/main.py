from contextlib import suppress

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from loader import dp, config


# Sample ecoho
@dp.message_handler(state="*")
async def echo(message: Message, state: FSMContext):
    with suppress():
        await state.finish()
    await message.answer(message.text)
