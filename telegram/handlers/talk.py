from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import utils.gpt as gpt
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

class FSMTalk(StatesGroup):
    talk=State()

async def talk_start(message : types.Message):
    await FSMTalk.talk.set()
    await message.reply('Да, я слушаю!')

async def talk_end(message : types.Message, state: FSMContext):
    await state.finish()
    await message.reply(gpt.talk_to_bot2(message.text))

def register_handlers_talk(dp: Dispatcher):
    dp.register_message_handler(talk_start, commands='talk', state=None)
    dp.register_message_handler(talk_end, state=FSMTalk.talk)