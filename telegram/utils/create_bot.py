from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import configparser
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

config = configparser.ConfigParser()
config.read(ROOT /'config.ini')

storage = MemoryStorage()

bot = Bot(token=config['DEFAULT']['TOKEN'])
dp = Dispatcher(bot, storage=storage) 
