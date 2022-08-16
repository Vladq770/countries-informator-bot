"""Loader of bot"""
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from settings import get_settings, Settings

config: Settings = get_settings()

bot = Bot(
    token=config.bot.BOT_API_TOKEN,
    parse_mode=types.ParseMode.HTML,
)
storage = RedisStorage2(**config.redis.storage_config, pool_size=50)
dp = Dispatcher(bot, storage=storage)
