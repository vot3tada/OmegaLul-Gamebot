from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


import configparser
config = configparser.ConfigParser()
config.read('./../config.ini')


storage = MemoryStorage()

#bot = Bot(token=config['DEFAULT']['TOKEN'])
bot = Bot('6292851990:AAExo7VLTMj62VEyurq5Dax3hj9oknqmrkM')
dp = Dispatcher(bot, storage=storage)
