from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import Classes.Player as Player
from utils.create_bot import dp, bot
import Classes.Task as Task
from utils.scheduler import scheduler
import random
import os
from handlers.collector import CollectorState
import handlers.achievement as AchievementHandler
from pathlib import Path
from utils import ParseSeconds

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]


class TaskState(StatesGroup):
    name = State()
    money = State()
    deadline = State()
    take = State()

async def taskList(message: types.Message):

    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Нужно зарегаться для такого')
        return
    
    tasks: list[Task.Task] = Task.GetFreeTasks(message.chat.id)
    replytext = '<b>Список заданий</b>:\n<i>Возьмите задание, выолните и попросите Заказчика зачесть\n</i>'
    keyboard = None
    for task in tasks[:4]:
        player = Player.GetPlayer(task.chatId, task.ownerUserId)
        time = ParseSeconds(task.duration)
        
        replytext += f"""
        Задание:  <i>{task.name}</i>
        Заказчик:  {player.name}
        Время на выполнение: {time}
        Награда:  {task.money} монет
        ID: {task.id}
        """
    if len(tasks) > 4:
        keyboard = types.InlineKeyboardMarkup()
        buttons: list[types.InlineKeyboardButton] = []
        buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
        buttons.append(types.InlineKeyboardButton(text='1', callback_data='@$^'))
        buttons.append( types.InlineKeyboardButton(text='След. ', callback_data=f'taskPage:1'))
        keyboard.row(*buttons)

    await message.answer_photo(
        photo= open(ROOT / 'static/tasklist/' / random.choice(os.listdir(ROOT / 'static/tasklist')) ,'rb'),
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

    tasks: list[Task.Task] = Task.GetFreeTasks()
    replytext = '<b>Список заданий</b>:\n<i>Возьмите задание, выолните и попросите Заказчика зачесть\n</i>'
    keyboard = None
    for task in tasks[page*4:page*4+4]:
        player = Player.GetPlayer(task.chatId, task.ownerUserId)
        time = ParseSeconds(task.duration)
        
        replytext += f"""
        Задание:  <i>{task.name}</i>
        Заказчик:  {player.name}
        Время на выполнение: {time}
        Награда:  {task.money} монет
        ID: {task.id}
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

async def myGivenTaskList(message: types.Message):

    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Нужно зарегаться для такого')
        return

    player: Player.Player = Player.GetPlayer(message.chat.id, message.from_user.id)
    tasks: list[Task.Task] = Task.GetPlayerGivenTasks(message.chat.id, message.from_user.id)
    replytext = f'<b>Список заданий {player.name}</b>:\n'
    keyboard = types.InlineKeyboardMarkup()
    for task in tasks[:5]:
        keyboard.add(
            types.InlineKeyboardButton(text=task.name, callback_data=f'taskGivenChoice:{task.id}')
        )
    if len(tasks) > 5:
        buttons: list[types.InlineKeyboardButton] = []
        buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
        buttons.append(types.InlineKeyboardButton(text='1', callback_data="@$^"))
        buttons.append(types.InlineKeyboardButton(text='След. ', callback_data=f'myGivenTaskPage:{message.chat.id}_{message.from_user.id}_1'))
        keyboard.row(*buttons)

    await message.answer(
        text=replytext,
        reply_markup=keyboard,
        parse_mode='HTML'
    )

async def pageMyGivenTaskList(call: types.CallbackQuery):
 
    chatId, userId, page = call.data.replace("myGivenTaskPage:",'').split('_')
    if call.message.chat.id != int(chatId) or call.from_user.id != int(userId):
        await call.answer('Это не ваш список')
        return
    try:
        page = int(page)
    except:
        await call.answer()
        return
    
    player: Player.Player = Player.GetPlayer(int(chatId), int(userId))
    tasks: list[Task.Task] = Task.GetPlayerGivenTasks(player.chatId, player.userId)

    keyboard = types.InlineKeyboardMarkup()
    for task in tasks[page*5:page*5+5]:
        keyboard.add(
            types.InlineKeyboardButton(text=task.name, callback_data=f'taskGivenChoice:{task.id}')
        )
    if len(tasks) > 5:
        buttons: list[types.InlineKeyboardButton] = []
        if page:
            buttons.append(types.InlineKeyboardButton(text='Пред. ', callback_data=f'myGivenTaskPage:{player.chatId}_{player.userId}_{page-1}'))
        else:
            buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
        buttons.append(types.InlineKeyboardButton(text=page+1, callback_data="@$^"))
        if len(tasks) > page*5 + 5:
            buttons.append(types.InlineKeyboardButton(text='След. ', callback_data=f'myGivenTaskPage:{player.chatId}_{player.userId}_{page+1}'))
        else:
            buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
        keyboard.row(*buttons)

    await call.message.edit_text(
        reply_markup=keyboard,
        text= f'<b>Список заданий {player.name}</b>:\n',
        parse_mode='HTML'
    )
    await call.answer()

async def choiceMyGivenTask(call: types.CallbackQuery):

    id = call.data.replace("taskGivenChoice:",'')
    try:
        id = int(id)
    except:
        await call.answer()
        return
    task: Task.Task = Task.GetTask(id)
    if not task:
        await call.answer('Задания не существует')
        return
    if call.message.chat.id != task.chatId or call.from_user.id != task.ownerUserId:
        await call.answer('Это не ваш список')
        return
    time = ParseSeconds(task.duration)
        
    replyText = f'<b>{task.name}</b>\nНаграда: {task.money} монет\nВремя на выполнение: {time}'
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add( types.InlineKeyboardButton(text='Отметить как выполненное', callback_data=f'acceptTask:{id}'))
    keyboard.add(types.InlineKeyboardButton(text='Удалить', callback_data=f'deleteTask:{id}'))
    keyboard.add( types.InlineKeyboardButton(text='Вернуться назад', callback_data=f'myGivenTaskPage:{task.chatId}_{task.ownerUserId}_0'))

    await call.message.edit_text(
        text=replyText,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    await call.answer()

async def acceptTask(call: types.CallbackQuery):

    id = call.data.replace("acceptTask:",'')
    try:
        id = int(id)
    except:
        await call.answer()
        return
    task: Task.Task = Task.GetTask(id)
    if not task:
        await call.answer('Задания не существует')
        return
    if call.message.chat.id != int(task.chatId) or call.from_user.id != int(task.ownerUserId):
        await call.answer('Это не ваш список')
        return
    if not task.workerUserId:
        await call.answer('Задание никто не взял')
        return
    worker: Player.Player = Player.GetPlayer(task.chatId, task.workerUserId)
    worker.money += task.money
    worker.exp += 40 + (task.money * 0.7)
    owner: Player.Player = Player.GetPlayer(task.chatId, task.ownerUserId)
    Task.AcceptTask(task)
    await AchievementHandler.AddHistory(chatId = worker.chatId, userId = worker.userId, totalMoney=task.money, totalExp=40 + (task.money * 0.7), totalEndedTasks=1)
    await call.message.answer_photo(
        photo=open(ROOT / 'static/taskcomplete/' / random.choice(os.listdir(ROOT / 'static/taskcomplete')) ,'rb'),
        caption=f'{worker.name} успешно выполняет задание от {owner.name}\n<b>Получено:</b>\nОпыт: {40 + (task.money * 0.7)}\nДеньги: {task.money}',
        parse_mode='HTML'
    )
    await call.answer()

async def deleteTask(call: types.CallbackQuery):

    id = call.data.replace("deleteTask:",'')
    try:
        id = int(id)
    except:
        await call.answer()
        return
    task: Task.Task = Task.GetTask(id)
    if not task:
        await call.answer('Задания не существует!')
        return
    if call.message.chat.id != int(task.chatId) or call.from_user.id != int(task.ownerUserId):
        await call.answer('Это не ваш список!')
        return
    if task.workerUserId:
        await call.answer('Задание кем то взято!')
        return
    player: Player.Player = Player.GetPlayer(task.chatId, task.ownerUserId)
    sale = 1 if (await call.message.chat.get_member(player.userId)).is_chat_admin() else 0
    player.money += (task.money - (0.5 * task.money * sale))
    Task.DeleteTask(task)
    call.data = f'myGivenTaskPage:{task.chatId}_{task.ownerUserId}_0'
    await pageMyGivenTaskList(call)

async def startTakeTask(message: types.Message):

    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Нужно зарегаться для такого')
        return
    
    await TaskState.take.set()

    await message.reply(
        text='Напишите номер задания, которое хотите взять.',
    )
    

async def endTakeTask(message: types.Message):
    worker = Player.GetPlayer(message.chat.id, message.from_user.id)
    id =  message.text.strip()
    try:
       id = int(id)
    except:
        await message.reply('Напишите корректно id задания, которое хотите взять')
        return
    
    if not Task.FindTask(id):
        await message.reply('Задания с таким id нема')
        return

    task: Task.Task = Task.GetTask(id)

    if task.workerUserId:
        await message.reply('Задание уже взято')
        return
    if task.ownerUserId == worker.userId:
        await message.reply('Нельзя взять свое задание')
        return
    
    Task.TakeTask(worker, task, punish)
    owner = Player.GetPlayer(task.chatId, task.ownerUserId)
    await message.answer(f'{worker.name} успешно берет задание от {owner.name}')
    await AchievementHandler.AddHistory(chatId = worker.chatId, userId = worker.userId, totalTakenTasks=1)
    scheduler.add_job(remind, trigger='interval', seconds=round(task.duration/3), args=[worker.chatId,worker.userId,task.id], id=f'remember_{worker.chatId}_{worker.userId}_{task.id}')

async def myTakenTaskList(message: types.Message):

    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Нужно зарегаться для такого')
        return

    player: Player.Player = Player.GetPlayer(message.chat.id, message.from_user.id)
    tasks: list[Task.Task] = Task.GetPlayerTakenTasks(message.chat.id, message.from_user.id)
    replytext = f'<b>Список заданий {player.name}</b>:\n'
    keyboard = types.InlineKeyboardMarkup()
    for task in tasks[:5]:
        keyboard.add(
            types.InlineKeyboardButton(text=task.name, callback_data=f'taskTakenChoice:{task.id}')
        )
    if len(tasks) > 5:
        buttons: list[types.InlineKeyboardButton] = []
        buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
        buttons.append(types.InlineKeyboardButton(text='1', callback_data="@$^"))
        buttons.append(types.InlineKeyboardButton(text='След. ', callback_data=f'myTakenTaskPage:{message.chat.id}_{message.from_user.id}_1'))
        keyboard.row(*buttons)

    await message.answer(
        text=replytext,
        reply_markup=keyboard,
        parse_mode='HTML'
    )

async def pageMyTakenTaskList(call: types.CallbackQuery):
 
    chatId, userId, page = call.data.replace("myTakenTaskPage:",'').split('_')
    if call.message.chat.id != int(chatId) or call.from_user.id != int(userId):
        await call.answer('Это не ваш список')
        return
    try:
        page = int(page)
    except:
        await call.answer()
        return
    
    player: Player.Player = Player.GetPlayer(int(chatId), int(userId))
    tasks: list[Task.Task] = Task.GetPlayerTakenTasks(player.chatId, player.userId)

    keyboard = types.InlineKeyboardMarkup()
    for task in tasks[page*5:page*5+5]:
        keyboard.add(
            types.InlineKeyboardButton(text=task.name, callback_data=f'taskTakenChoice:{task.id}')
        )
    if len(tasks) > 5:
        buttons: list[types.InlineKeyboardButton] = []
        if page:
            buttons.append(types.InlineKeyboardButton(text='Пред. ', callback_data=f'myTakenTaskPage:{player.chatId}_{player.userId}_{page-1}'))
        else:
            buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
        buttons.append(types.InlineKeyboardButton(text=page+1, callback_data="@$^"))
        if len(tasks) > page*5 + 5:
            buttons.append(types.InlineKeyboardButton(text='След. ', callback_data=f'myTakenTaskPage:{player.chatId}_{player.userId}_{page+1}'))
        else:
            buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
        keyboard.row(*buttons)

    await call.message.edit_text(
        reply_markup=keyboard,
        text= f'<b>Список заданий {player.name}</b>:\n',
        parse_mode='HTML'
    )
    await call.answer()

async def choiceMyTakenTask(call: types.CallbackQuery):

    id = call.data.replace("taskTakenChoice:",'')
    try:
        id = int(id)
    except:
        await call.answer()
        return
    task: Task.Task = Task.GetTask(id)
    if not task:
        await call.answer('Задания не существует')
        return
    if call.message.chat.id != task.chatId or call.from_user.id != task.workerUserId:
        await call.answer('Это не ваш список')
        return
    time = ParseSeconds(task.duration)
        
    replyText = f'<b>{task.name}</b>\nНаграда: {task.money} монет\nВремя на выполнение: {time}'
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Отказаться', callback_data=f'refuseTask:{id}'))
    keyboard.add( types.InlineKeyboardButton(text='Вернуться назад', callback_data=f'myTakenTaskPage:{task.chatId}_{task.workerUserId}_0'))

    await call.message.edit_text(
        text=replyText,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    await call.answer()

async def refuseTask(call: types.CallbackQuery):

    id = call.data.replace("refuseTask:",'')
    try:
        id = int(id)
    except:
        await call.answer()
        return
    task: Task.Task = Task.GetTask(id)
    if not task:
        await call.answer('Задания не существует!')
        return
    if call.message.chat.id != task.chatId or call.from_user.id != task.workerUserId:
        await call.answer('Это не ваше задание!')
        return
    
    player: Player.Player = Player.GetPlayer(task.chatId, task.workerUserId)
    if Task.RefuseTask(player, task):
        await call.message.answer(f'{player.name} получает наказание за столь позднюю отмену задания...')
        await AchievementHandler.AddHistory(chatId = player.chatId, userId = player.userId, totalFallTasks=1)
    call.data = f'myTakenTaskPage:{player.chatId}_{player.userId}_0'
    if scheduler.get_job(job_id=f'remember_{player.chatId}_{player.userId}_{task.id}'):
        scheduler.remove_job(f'remember_{player.chatId}_{player.userId}_{task.id}')
    await pageMyTakenTaskList(call)

async def startAddTask(message: types.Message):
    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Нужно зарегаться для такого')
        return
    await TaskState.name.set()
    await message.reply(text='Введите название (оно же описание) задания')

async def setTaskName(message: types.Message, state: FSMContext):
    if message.text == '':
        await message.reply(text='Описание не может быть пустым')
        return
    if len(message.text) > 150:
        await message.reply(text='Описание слишком больше, формулируйте лаконичнее!')
        return
    async with state.proxy() as data:
        data['name'] = message.text
    await message.reply(text='Введите награду, которую вы заплатите из своего кармана!\n(Админы платят половину от указанной суммы)')
    await TaskState.money.set()

async def setTaskMoney(message: types.Message, state: FSMContext):
    try:
        money = int(message.text)
    except:
        await message.reply(text='Цыферками денюшки надо ввести')
        return
    player: Player.Player = Player.GetPlayer(message.chat.id, message.from_user.id)
    if money < 0:
        await message.reply(text='Награда не может быть отрицательная, но Коллектор оценил')
        return
    if money > player.money:
        await message.reply(text='У вас нет столько денежек')
        return

    async with state.proxy() as data:
        data['money'] = money
    await message.reply(text='Введите время выполненения задания в виде: ДД/ЧЧ/ММ')
    await TaskState.deadline.set()

async def setTaskDeadline(message: types.Message, state: FSMContext):
    timetext = message.text.split('/')
    try:
        time: int = 86400 * int(timetext[0]) + 3600 * int(timetext[1]) + 60 * int(timetext[2])
    except:
        await message.reply('Неправильный формат даты: ДД/ЧЧ/ММ')
        return
    
    if time < 60:
        await message.reply('Слишком мало времени на задание, не будьте так жестоки!!')
        return

    player: Player.Player = Player.GetPlayer(message.chat.id, message.from_user.id)
    sale = 1 if (await message.chat.get_member(player.userId)).is_chat_admin() else 0
    async with state.proxy() as data:
        task = Task.Task(
            data['name'],
            message.chat.id,
            message.from_user.id,
            -1,
            data['money'],
            time
        )
        player.money -= (data['money'] - (0.5 * data['money'] * sale))
    Task.AddTask(task)
    await state.finish()
    
    await message.reply_photo(
        photo=open(ROOT / 'static/taskadd/' / random.choice(os.listdir(ROOT / 'static/taskadd')) ,'rb'),
        caption=f'Задание от {player.name} успешно добавлено на доску')
    
async def cancelAddingTask(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Отменено')

async def remind(chatId: int, userId: int, taskId: int):
    scheduler.remove_job(f'remember_{chatId}_{userId}_{taskId}')
    task = Task.GetTask(taskId)
    if not task:
        return
    durationLeft = task.duration / 3
    time = ParseSeconds(durationLeft)

    await bot.send_photo(
        chat_id=userId,
        parse_mode='HTML',
        photo=open(ROOT / 'static/remind/' / random.choice(os.listdir(ROOT / 'static/remind')) ,'rb'),
        caption=f'Надеюсь вы не забыли про ваше задание <i>{task.name}</i> ?\nУ вас осталось {time} времени на выполнение.'
    )

async def punish(chatId: int, userId: int, taskId: int):
    
    st : FSMContext = dp.current_state(chat=chatId, user=userId)
    task = Task.GetTask(taskId)
    if (await st.get_state()):
        return
    scheduler.remove_job(f'punish_{task.chatId}_{userId}_{task.id}')
    await st.set_state(CollectorState.Punished)

    Task.FreeTask(Task.GetTask(taskId))

    player: Player.Player = Player.GetPlayer(chatId, userId)
    keyboard = types.InlineKeyboardMarkup()
    
    if player.money >= (task.money // 2):#Можно и в одну строчку
        payText =  'Заплатить'  
    else:
        payText = 'Заплатить что есть'
    keyboard.add(
        types.InlineKeyboardButton(text=payText, callback_data=f'collectorPay:{player.chatId}_{player.userId}_{task.money // 2}')
    )
    keyboard.add(
        types.InlineKeyboardButton(text='Сразиться', callback_data=f'collectorFight:{player.chatId}_{player.userId}_{task.money // 2}')
    )
    username: str = (await bot.get_chat_member(chatId, userId)).user.username
    message = await bot.send_photo(chat_id=chatId,
                     parse_mode='HTML',
                     reply_markup=keyboard,
                     photo = open(ROOT / 'static/collector/T801.jpg','rb'),
                     caption=f'''<i>Он пришел...</i>
                     
Коллектор пришел по твою душу, {player.name}, и взял тебя в заложники!
@{username} У тебя есть выбор:\n
<b>Заплатить</b> сумму {task.money // 2} и мирно разойтись
<b>Драться</b> за свою свободу''',
                     )
    await st.set_data(
        {'messageId':  message.message_id}
    )

def register_handlers_task(dp: Dispatcher):
    dp.register_message_handler(cancelAddingTask, commands='cancel', state=[TaskState.name, TaskState.money, TaskState.deadline, TaskState.take])
    dp.register_message_handler(taskList, commands='task', state=None)
    dp.register_callback_query_handler(pageTaskList, regexp='^taskPage:*', state=None)
    dp.register_message_handler(myGivenTaskList,commands='task_given', state=None)
    dp.register_callback_query_handler(pageMyGivenTaskList, regexp='^myGivenTaskPage:*', state=None)
    dp.register_callback_query_handler(choiceMyGivenTask, regexp='^taskGivenChoice:*', state=None)
    dp.register_callback_query_handler(acceptTask, regexp='^acceptTask:*', state=None)
    dp.register_callback_query_handler(deleteTask, regexp='^deleteTask:*', state=None)
    dp.register_message_handler(startTakeTask, commands='task_take', state=None)
    dp.register_message_handler(endTakeTask, state=TaskState.take)
    dp.register_message_handler(myTakenTaskList,commands='task_taken', state=None)
    dp.register_callback_query_handler(pageMyTakenTaskList, regexp='^myTakenTaskPage:*', state=None)
    dp.register_callback_query_handler(choiceMyTakenTask, regexp='^taskTakenChoice:*', state=None)
    dp.register_callback_query_handler(refuseTask, regexp='^refuseTask:*', state=None)
    dp.register_message_handler(startAddTask, commands='task_add', state=None)
    dp.register_message_handler(setTaskName, state=TaskState.name)
    dp.register_message_handler(setTaskMoney, state=TaskState.money)
    dp.register_message_handler(setTaskDeadline, state=TaskState.deadline)