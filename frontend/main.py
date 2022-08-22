"""Start file of app"""
# !/usr/bin/env python
from aiogram import executor
from aiogram.types import Message
from handlers import dp
from utils.dependencies import get_aiohttp_client_session

from utils.setup_logging import setup_logging


async def on_startup(dispatcher):
    ...


async def on_shutdown(dispatcher):
    await get_aiohttp_client_session().close()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == "__main__":
    setup_logging()
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
