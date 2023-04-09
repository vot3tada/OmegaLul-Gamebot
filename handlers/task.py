from datetime import datetime
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from utils.create_bot import dp, bot
import Classes.Player as Player
import Classes.Task as Task
from utils.scheduler import scheduler
from dateutil import tz

class TaskState(StatesGroup):
    name = State()
    money = State()
    deadline = State()

async def taskList(message: types.Message):
    pass

async def startAddTask(message: types.Message, state: FSMContext):
    await TaskState.name.set()
    await message.reply(text='Введите название (оно же описание) задания')

async def setTaskName(message: types.Message, state: FSMContext):
    if message.text == '':
        await message.reply(text='Описание не может быть пустым')
        return
    async with state.proxy() as data:
        data['name'] = message.text
    await message.reply(text='Введите награду, которую вы заплатите из своего кармана')
    await TaskState.money.set()

async def setTaskMoney(message: types.Message, state: FSMContext):
    try:
        money = int(message.text)
    except:
        await message.reply(text='Цыферками денюшки надо ввести')
        return
    player: Player.Player = Player.GetPlayer(message.chat.id, message.from_user.id)
    if money > player.money:
        await message.reply(text='У вас нет столько денежек')
        return

    async with state.proxy() as data:
        data['money'] = money
    await message.reply(text='Введите дедлайн в форме: ГГГГ/ММ/ДД/ЧЧ/ММ')
    await TaskState.deadline.set()

async def setTaskDeadline(message: types.Message, state: FSMContext):
    datetext = message.text.split('/')
    try:
        date = datetime(int(datetext[0]), int(datetext[1]), int(datetext[2]), int(datetext[3]), int(datetext[4]), tzinfo=tz.gettz("Europe/Moscow"))
    except:
        await message.reply('Неправильный формат даты: ГГГГ/ММ/ДД/ЧЧ/ММ')
        return
    
    if date < datetime.now(tz.gettz("Europe/Moscow")):
        await message.reply('Указана дата из прошлого: будьте аккуратны с парадоксами')
        return
    
    async with state.proxy() as data:
        task = Task.Task(
            data['name'],
            message.chat.id,
            message.from_user.id,
            -1,
            date,
            data['money']
        )
    Task.AddTask(task)
    player: Player.Player = Player.GetPlayer(message.chat.id, message.from_user.id)
    await message.reply(f'Задание от {player.name} успешно добавлено на доску')


def register_handlers_task(dp: Dispatcher):
    dp.register_message_handler(taskList, commands='task', state=None)
    dp.register_message_handler(startAddTask, commands='task_add', state=None)
    dp.register_message_handler(startAddTask, commands='task_cancel', state=[TaskState.name, TaskState.money, TaskState.deadline])
    dp.register_message_handler(setTaskName, state=TaskState.name)
    dp.register_message_handler(setTaskMoney, state=TaskState.money)
    dp.register_message_handler(setTaskDeadline, state=TaskState.deadline)