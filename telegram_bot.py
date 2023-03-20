"""
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

"""
"""
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Event(StatesGroup):
    name = State()

chats = dict()


storage = MemoryStorage()



import configparser
config = configparser.ConfigParser()
config.read('config.ini')




bot = Bot(token=config['DEFAULT']['TOKEN'])
dp = Dispatcher(bot, storage=storage)





@dp.message_handler(commands='Эхо')
async def echo_start(message : types.Message, state: FSMContext):
    await storage.set_state(chat=message.chat.id, user=message.from_user.id, state=state)
    await message.answer('Папугай включен')
    async with state.proxy() as data:
        data['name'] = 'play'


@dp.message_handler(commands='ЭхоОфф')
async def echo_end(message : types.Message, state: FSMContext):
    await message.answer('Папугай выключен')
    await state.finish()


@dp.message_handler()
async def echo_send(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data and data['name'] == 'play':
            await message.answer(message.from_user.first_name +': '+message.text)
    





executor.start_polling(dp, skip_updates = True)
"""
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Event(StatesGroup):
    name = State()

chats = dict()


storage = MemoryStorage()

import configparser
config = configparser.ConfigParser()
config.read('config.ini')




bot = Bot(token=config['DEFAULT']['TOKEN'])
dp = Dispatcher(bot, storage=storage)





@dp.message_handler(commands='Эхо')
async def echo_start(message : types.Message, state: FSMContext):
    await message.answer('Папугай включен')
    #async with state.proxy() as data:
    #    data['name'] = 'play'
    chats[str(message.chat.id)] = 'echo'
    print(chats)


@dp.message_handler(commands='ЭхоОфф')
async def echo_end(message : types.Message, state: FSMContext):
    await message.answer('Папугай выключен')
    #await state.finish()
    chats[str(message.chat.id)] = None


@dp.message_handler()
async def echo_send(message : types.Message):
    #async with state.proxy() as data:
        #if data and data['name'] == 'play':
    print(message.chat.id)
    if str(message.chat.id) in chats and chats[str(message.chat.id)]:
        await message.answer(message.from_user.first_name +': '+message.text)
    





executor.start_polling(dp, skip_updates = True)