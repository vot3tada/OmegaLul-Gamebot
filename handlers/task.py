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
import random
import os

class TaskState(StatesGroup):
    name = State()
    money = State()
    deadline = State()

async def taskList(message: types.Message):

    tasks: list[Task.Task] = Task.GetAllTasks()
    replytext = '<b>Список заданий</b>:\n<i>Выволните задание и покажите заказчику, он вам засчитает\n</i>'
    keyboard = None
    for task in tasks[:4]:
        player = Player.GetPlayer(task.chatId, task.userId)
        replytext += f"""
        Задание:  <i>{task.name}</i>
        Заказчик:  {player.name}
        Награда:  {task.money} монет
        """
    if len(tasks) > 4:
        keyboard = types.InlineKeyboardMarkup()
        buttons: list[types.InlineKeyboardButton] = []
        buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
        buttons.append(types.InlineKeyboardButton(text='1', callback_data='@$^'))
        buttons.append( types.InlineKeyboardButton(text='След. ', callback_data=f'taskPage:1'))
        keyboard.row(*buttons)

    await message.answer_photo(
        photo= open('./static/tasklist/' + random.choice(os.listdir('./static/tasklist')) ,'rb'),
        caption=replytext,
        parse_mode='HTMl',
        reply_markup=keyboard
    )

async def pageTaskList(call: types.CallbackQuery):
    
    page = call.data.replace("taskPage:",'')
    try:
        page = int(page)
    except:
        await call.answer()
        return

    tasks: list[Task.Task] = Task.GetAllTasks()
    replytext = '<b>Список заданий</b>:\n<i>Выволните задание и покажите заказчику, он вам засчитает\n</i>'
    keyboard = None
    for task in tasks[page*4:page*4+4]:
        player = Player.GetPlayer(task.chatId, task.userId)
        replytext += f"""
        Задание:  <i>{task.name}</i>
        Заказчик:  {player.name}
        Награда:  {task.money} монет
        """
    if len(tasks) > 4:
        keyboard = types.InlineKeyboardMarkup()
        buttons: list[types.InlineKeyboardButton] = []
        if page:
            buttons.append(types.InlineKeyboardButton(text='Пред. ', callback_data=f'taskPage:{page-1}'))
        else:
            buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
        buttons.append(types.InlineKeyboardButton(text=page+1, callback_data="@$^"))
        if len(tasks) > page*4 + 4:
            buttons.append(types.InlineKeyboardButton(text='След. ', callback_data=f'taskPage:{page+1}'))
        else:
            buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
        keyboard.row(*buttons)

    await call.message.edit_caption(
        caption=replytext,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    await call.answer()

async def myTaskList(message: types.Message):

    player: Player.Player = Player.GetPlayer(message.chat.id, message.from_user.id)
    tasks: list[Task.Task] = Task.GetPlayerTasks(message.chat.id, message.from_user.id)
    replytext = f'<b>Список заданий {player.name}</b>:\n'
    keyboard = types.InlineKeyboardMarkup()
    for task in tasks[:5]:
        keyboard.add(
            types.InlineKeyboardButton(text=task.name, callback_data=f'taskChoice:{task.id}')
        )
    if len(tasks) > 5:
        buttons: list[types.InlineKeyboardButton] = []
        buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
        buttons.append(types.InlineKeyboardButton(text='1', callback_data="@$^"))
        buttons.append(types.InlineKeyboardButton(text='След. ', callback_data=f'myTaskPage:{message.chat.id}_{message.from_user.id}_1'))
        keyboard.row(*buttons)

    await message.answer(
        text=replytext,
        reply_markup=keyboard,
        parse_mode='HTML'
    )

async def pageMyTaskList(call: types.CallbackQuery):

    chatId, userId, page = call.data.replace("myTaskPage:",'').split('_')
    if call.message.chat.id != int(chatId) or call.from_user.id != int(userId):
        await call.answer('Это не ваш список')
        return
    try:
        page = int(page)
    except:
        await call.answer()
        return

    player: Player.Player = Player.GetPlayer(int(chatId), int(userId))
    tasks: list[Task.Task] = Task.GetPlayerTasks(player.chatId, player.userId)

    keyboard = types.InlineKeyboardMarkup()
    for task in tasks[page*5:page*5+5]:
        keyboard.add(
            types.InlineKeyboardButton(text=task.name, callback_data=f'taskChoice:{task.id}')
        )
    if len(tasks) > 5:
        buttons: list[types.InlineKeyboardButton] = []
        if page:
            buttons.append(types.InlineKeyboardButton(text='Пред. ', callback_data=f'myTaskPage:{player.chatId}_{player.userId}_{page-1}'))
        else:
            buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
        buttons.append(types.InlineKeyboardButton(text=page+1, callback_data="@$^"))
        if len(tasks) > page*5 + 5:
            buttons.append(types.InlineKeyboardButton(text='След. ', callback_data=f'myTaskPage:{player.chatId}_{player.userId}_{page+1}'))
        else:
            buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
        keyboard.row(*buttons)

    await call.message.edit_reply_markup(
        reply_markup=keyboard
    )
    await call.answer()

async def choiceMyTask(call: types.CallbackQuery):

    id = call.data.replace("taskChoice:",'')
    try:
        id = int(id)
    except:
        await call.answer()
        return
    task: Task.Task = Task.GetTask(id)
    if not task:
        await call.answer('Задания не существует')
        return
    if call.message.chat.id != int(task.chatId) or call.from_user.id != int(task.userId):
        await call.answer('Это не ваш список')
        return
    
    replyText = f'<b>{task.name}</b>\nНаграда: {task.money} монет\nДата закрытия: {task.deadline.day}/{task.deadline.month} в {task.deadline.hour} ч.'
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add( types.InlineKeyboardButton(text='Отметить как выполненное', callback_data=f'acceptTask:{id}'))
    keyboard.add(types.InlineKeyboardButton(text='Удалить', callback_data=f'deleteTask:{id}'))
    keyboard.add( types.InlineKeyboardButton(text='Вернуться назад', callback_data=f'myTaskPage:{task.chatId}_{task.userId}_0'))

    await call.message.edit_text(
        text=replyText,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    await call.answer()

async def startCloseTask(call: types.CallbackQuery, state: FSMContext):
    pass

async def endCloseTask(message: types.Message, state: FSMContext):
    pass

async def deleteTask(call: types.CallbackQuery):
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
    await message.reply(text='Введите награду, которую вы заплатите из своего кармана!\n(Админ платит половину от указанной суммы)')
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
    await message.reply(text='Введите дедлайн в форме: ГГГГ/ММ/ДД/ЧЧ')
    await TaskState.deadline.set()

async def setTaskDeadline(message: types.Message, state: FSMContext):
    datetext = message.text.split('/')
    try:
        date = datetime(int(datetext[0]), int(datetext[1]), int(datetext[2]), int(datetext[3]), tzinfo=tz.gettz("Europe/Moscow"))
    except:
        await message.reply('Неправильный формат даты: ГГГГ/ММ/ДД/ЧЧ')
        return
    
    if date < datetime.now(tz.gettz("Europe/Moscow")):
        await message.reply('Указана дата из прошлого: будьте аккуратны с парадоксами')
        return
    player: Player.Player = Player.GetPlayer(message.chat.id, message.from_user.id)
    async with state.proxy() as data:
        task = Task.Task(
            data['name'],
            message.chat.id,
            message.from_user.id,
            -1,
            date,
            data['money']
        )
        player.money -= data['money']
    Task.AddTask(task)
    await state.finish()
    
    await message.reply_photo(
        photo=open('./static/taskadd/' + random.choice(os.listdir('./static/taskadd')) ,'rb'),
        caption=f'Задание от {player.name} успешно добавлено на доску')
    
def cancelAddingTask(message: types.Message, state: FSMContext):
    state.finish()
    message.reply('Создание задания отменено')

def register_handlers_task(dp: Dispatcher):
    dp.register_message_handler(taskList, commands='task', state=None)
    dp.register_callback_query_handler(pageTaskList, regexp='^taskPage:*', state=None)
    dp.register_message_handler(myTaskList,commands='task_my', state=None)
    dp.register_callback_query_handler(pageMyTaskList, regexp='^myTaskPage:*', state=None)
    dp.register_callback_query_handler(choiceMyTask, regexp='^taskChoice:*', state=None)
    dp.register_message_handler(startAddTask, commands='task_add', state=None)
    dp.register_message_handler(cancelAddingTask, commands='task_cancel', state=[TaskState.name, TaskState.money, TaskState.deadline])
    dp.register_message_handler(setTaskName, state=TaskState.name)
    dp.register_message_handler(setTaskMoney, state=TaskState.money)
    dp.register_message_handler(setTaskDeadline, state=TaskState.deadline)