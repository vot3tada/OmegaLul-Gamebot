from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from utils.create_bot import dp, bot
import Classes.Player as Player
from utils.scheduler import scheduler

async def TaskList(message: types.Message):
    pass

async def AddTask(message: types.Message, state: FSMContext):
    pass


def register_handlers_task(dp: Dispatcher):
    dp.register_message_handler(TaskList, commands='task', state=None)
    dp.register_message_handler(AddTask, commands='task_add', state=None)