from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

storage = MemoryStorage()

bot = Bot(token=config['DEFAULT']['TOKEN'])
dp = Dispatcher(bot, storage=storage) 
