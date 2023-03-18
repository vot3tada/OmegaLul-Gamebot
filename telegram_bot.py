from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import configparser
config = configparser.ConfigParser()
config.read('config.ini')




bot = Bot(token=config['DEFAULT']['TOKEN'])
dp = Dispatcher(bot)




@dp.message_handler()
async def echo_send(message : types.Message):
    await message.answer(message.from_user.first_name +': '+message.text)
    





executor.start_polling(dp, skip_updates = True)