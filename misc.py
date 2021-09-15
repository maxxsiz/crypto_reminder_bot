import logging
from aiogram import Bot, Dispatcher
from settings import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

