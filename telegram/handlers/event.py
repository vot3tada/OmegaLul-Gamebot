from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import Classes.Event as Event
from datetime import datetime
from utils.scheduler import scheduler
import Classes.Player as Player
from utils.create_bot import bot, dp
import random
import os
import handlers.achievement as AchievementHandler
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

class FSMEvent(StatesGroup):
    name = State()
    date = State()
    addplayers = State()
    inEvent = State()
    admin = State()
    delete = State()

async def event_start(message : types.Message):
    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Нужно зарегаться для такого')
        return
    await FSMEvent.name.set()
    await message.reply('Напишите название мероприятия')

async def event_set_date(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMEvent.date.set()
    await message.reply('Напишите дату и время мероприятия в формате: ГГГГ/ММ/ДД/ЧЧ/ММ')

async def event_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Отменено')

async def event_delete_start(message : types.Message, state: FSMContext):
    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Нужно зарегаться для такого')
        return
    await FSMEvent.delete.set()
    await message.answer('Напишите номер эвента')

async def event_delete_end(message : types.Message, state: FSMContext):
    try:
        event = Event.GetEvent(message.text)
    except:
        await message.answer('Неправильный номер')
        return
    if (event == None):
        await message.answer('Такого эвента не существует')
        return
    player : Player.Player = Player.GetPlayer(message.chat.id, message.from_user.id)
    if (event.chatId != player.chatId or event.userId != player.userId):
        await message.answer('Вы не являетесь создателем этого эвента')
        return
    Event.RemoveEvent(event.id)
    scheduler.remove_job('e'+str(event.id)+'-')
    scheduler.remove_job('e'+str(event.id)+'--')
    await state.finish()
    await message.answer('Эвент отменен')
    

async def event_end(message : types.Message, state: FSMContext):
    from dateutil import tz
    async with state.proxy() as data:
        name = data['name']
    date = message.text.split('/')
    try:
        time = datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]), tzinfo=tz.gettz("Europe/Moscow"))
    except:
        await message.reply('Неправильный формат даты: ГГГГ/ММ/ДД/ЧЧ/ММ')
        return
    if len([i for i in Event.GetAllEvents(message.chat.id) if abs((time-i.datetime).total_seconds()) < 600]) > 0:
        await message.reply('В это время уже существует эвент')
        return
    event = Event.Event(0, name, f'{date[0]}-{date[1]}-{date[2]} {date[3]}:{date[4]}:00', [])
    event.chatId = message.chat.id
    event.userId = message.from_user.id
    event = Event.AddEvent(event)
    await state.finish()
    await AchievementHandler.AddHistory(chatId = message.chat.id, userId = message.from_user.id, totalCreateEvent=1)
    await message.reply(f'Мероприятие с #{event.id} создано')
    await bot.send_photo(chat_id=message.chat.id,  
                        caption=f'<b>ВСЕ! ВСЕ! ВСЕ!</b>\nУслышьте! Этого числа <b>{time:%d.%m.%Y}</b> ' /
                        f'в <b>{time:%H:%M}</b> состоится эвент:\n<b>{event.name}</b>!\n' /
                        'Не опаздывайте! Награда ждет посетителей!', 
                        photo=open(ROOT / 'static/anonce/' / random.choice(os.listdir(ROOT / 'static/anonce')) ,'rb'),
                        parse_mode='HTML')
    
    for i in Player.GetAllPlayers(message.chat.id):
        await bot.send_photo(chat_id=i.userId, 
                               caption=f'Услышьте! Этого числа <b>{time:%d.%m.%Y}</b> ' /
                                f'в <b>{time:%H:%M}</b> состоится эвент:\n<b>{event.name}</b>!\n' /
                                'Не опаздывайте! Награда ждет посетителей!',
                               parse_mode='HTML',
                               photo=open(ROOT / 'static/meeting/' / random.choice(os.listdir(ROOT / 'static/meeting')) ,'rb'))

    scheduler.add_job(trigger_before_event, 'date', run_date= 
                      datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]) - 1, int(date[4]), 
                                                                        tzinfo=tz.gettz("Europe/Moscow")), args=[message.chat.id, event.name], id=('e'+str(event.id)+'-'))
    scheduler.add_job(trigger_event, 'date', run_date= datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]), 
                                                                        tzinfo=tz.gettz("Europe/Moscow")), args=[message.chat.id, event.id], id=('e'+str(event.id)+'--'))

async def trigger_before_event(chatId: int, eventName: str):
    await bot.send_photo(chat_id=chatId, 
                               caption=f'Через час пройдет эвент:\n <b>{eventName}</b>!\n Присоединяйтесь', 
                               parse_mode='HTML',
                               photo=open(ROOT / 'static/meeting/' / random.choice(os.listdir(ROOT / 'static/meeting')) ,'rb'))
    for i in Player.GetAllPlayers(chatId):
        await bot.send_photo(chat_id=i.userId, 
                               caption=f'Через час пройдет эвент:\n <b>{eventName}</b>!\n Присоединяйтесь', 
                               parse_mode='HTML',
                               photo=open(ROOT / 'static/meeting/' / random.choice(os.listdir(ROOT / 'static/meeting')) ,'rb'))

async def trigger_event(chatId: int, eventId: int):
    event = Event.GetEvent(eventId)
    photo = open(ROOT / 'static/meeting/' / random.choice(os.listdir(ROOT / 'static/meeting')) ,'rb')
    await bot.send_photo(chat_id=chatId,  
                            caption=f'Сейчас проходит эвент:\n<b>{event.name}</b>.\nУ вас есть пять минут проставить плюсики. Всем посетителям награда!', 
                            photo=photo,
                            parse_mode='HTML')
      
    for i in Player.GetAllPlayers(chatId):
        await bot.send_photo(chat_id=i.userId, 
                               caption=f'Сейчас проходит эвент:\n <b>{event.name}</b>!\n Присоединяйтесь', 
                               parse_mode='HTML',
                               photo=open(ROOT / 'static/meeting/' / random.choice(os.listdir(ROOT / 'static/meeting')) ,'rb'))
        st : FSMContext = dp.current_state(chat = i.chatId, user = i.userId)
        statePlayer = await st.get_state()
        if statePlayer == None:
            await st.set_state(FSMEvent.addplayers)
            await st.set_data(event.id)
    st : FSMContext = dp.current_state(chat = event.chatId, user = event.userId)
    await st.set_state(FSMEvent.admin)
    await st.set_data(event.id)
    scheduler.add_job(event_set_state, trigger='interval', seconds=2, jobstore='local', args=[event.chatId, eventId], coalesce=True, id=f'event:{eventId}reload')
    scheduler.add_job(scheduler_end, trigger='interval', seconds=300, jobstore='local', args=[event.chatId, eventId], coalesce=True, id=f'event:{eventId}end')

async def event_add_players(message : types.Message, state: FSMContext):
    eventId = await state.get_data()
    player: Player.Player = Player.GetPlayer(message.chat.id, message.from_user.id)
    Event.AddUser(eventId, chatId=message.chat.id, userId=message.from_user.id)
    await message.reply(f'{player.name} подключился')
    await FSMEvent.inEvent.set()

async def admin_end(message : types.Message, state: FSMContext):
    for i in Player.GetAllPlayers(message.chat.id):
        st : FSMContext = dp.current_state(chat = i.chatId, user = i.userId)
        statePlayer = await st.get_state()
        if statePlayer == FSMEvent.addplayers.state or statePlayer == FSMEvent.inEvent.state:
            await st.set_data(None)
            await dp.current_state(chat = i.chatId, user = i.userId).set_state(None)
    eventId = await state.get_data()
    event = Event.GetEvent(eventId)
    text = 'Посетители эвента:'
    for i in event.players:
        i.money += 50
        i.exp += 50
        await AchievementHandler.AddHistory(chatId = i.chatId, userId = i.userId, totalMoney=50, totalExp=50, totalEnterEvent=1)
        text += f'\n {i.name}'
    await message.answer('Регистрация на эвент завершена\n' / text + '\nКаждый посетитель получил:\n50 опыта\n50 монет')
    scheduler.remove_job(f'event:{eventId}end')
    scheduler.remove_job(f'event:{eventId}reload')
    await state.finish()

async def scheduler_end(chatId: int, eventId):
    for i in Player.GetAllPlayers(chatId):
        st : FSMContext = dp.current_state(chat = i.chatId, user = i.userId)
        statePlayer = await st.get_state()
        if statePlayer == FSMEvent.addplayers.state or statePlayer == FSMEvent.admin.state or statePlayer == FSMEvent.inEvent.state:
            await st.set_data(None)
            await dp.current_state(chat = i.chatId, user = i.userId).set_state(None)
    event = Event.GetEvent(eventId)
    text = 'Посетители эвента:'
    for i in event.players:
        i.money += 50
        i.exp += 50
        await AchievementHandler.AddHistory(chatId = i.chatId, userId = i.userId, totalMoney=50, totalExp=50)
        text += f'\n {i.name}'
    await bot.send_message(chat_id=chatId, text='Регистрация на эвент завершена\n' / text + '\nКаждый посетитель получил:\n50 опыта\n50 монет')
    scheduler.remove_job(f'event:{eventId}end')
    scheduler.remove_job(f'event:{eventId}reload')

async def admin_kick(message : types.Message, state: FSMContext):
    eventId = await state.get_data()
    event = Event.GetEvent(eventId)
    if not message.reply_to_message is None:
        eventUserId = [i.userId for i in event.players]
        if message.reply_to_message.from_user.id in eventUserId:
            Event.KickUser(eventId, chatId=message.chat.id, userId=message.reply_to_message.from_user.id)
            await message.reply(f'Выписан из движа')
            await AchievementHandler.AddHistory(chatId = message.chat.id, userId = message.from_user.id, totalKickEvent=1)
        else:
            await message.reply('Такой чел не в эвенте')
    else:
        await message.reply('Вы не выделили человечка')


async def event_set_state(chatId: int, eventId):
    for i in Player.GetAllPlayers(chatId):
        st : FSMContext = dp.current_state(chat = i.chatId, user = i.userId)
        statePlayer = await st.get_state()
        if statePlayer == None:
            await st.set_state(FSMEvent.addplayers)
            await st.set_data(eventId)

async def event_get_all(message : types.Message):
    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Нужно зарегаться для такого')
        return
    events = Event.GetAllEvents(message.chat.id)
    replytext = 'Список эвентов:'
    for i in events[:9]:
        replytext += f'\n<b>#{i.id}</b> - {i.name} - {i.datetime}'
    if (len == 0):
        message.answer('Нет эвентов в этом чате🤔')
        return
    buttons: list[types.InlineKeyboardButton] = []
    buttons.append(types.InlineKeyboardButton(text=' ', callback_data=f'@$^'))
    if (len(events) > 10):
        buttons.append(types.InlineKeyboardButton(text='>', callback_data=f'eventPages:{message.chat.id}_{message.from_user.id}_2'))
    else:
        buttons.append(types.InlineKeyboardButton(text=' ', callback_data=f'@$^'))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(*buttons)
    await message.answer(
        text=replytext,
        reply_markup=keyboard,
        parse_mode='HTML'
    )

async def event_get_all_pages(call: types.CallbackQuery):
    chatId, userId, page = call.data.replace("eventPages:",'').split('_')
    if call.message.chat.id != int(chatId) or call.from_user.id != int(userId):
        await call.answer('Это не ваш список')
        return
    try:
        page = int(page)
    except:
        await call.answer()
        return  
    events = Event.GetAllEvents(call.message.chat.id)
    replytext = 'Список эвентов:'
    for i in events[(page-1)*10:(page*10)-1]:
        replytext += f'\n<b>#{i.id}</b> - {i.name} - {i.datetime}'
    buttons: list[types.InlineKeyboardButton] = []
    if (page - 1 < 1):
        buttons.append(types.InlineKeyboardButton(text=' ', callback_data=f'@$^'))
    else:
        buttons.append(types.InlineKeyboardButton(text='<', callback_data=f'eventPages:{call.message.chat.id}_{call.from_user.id}_{page - 1}'))
    if (page*10 < len(events)):
        buttons.append(types.InlineKeyboardButton(text='>', callback_data=f'eventPages:{call.message.chat.id}_{call.from_user.id}_{page + 1}'))
    else:
        buttons.append(types.InlineKeyboardButton(text=' ', callback_data=f'@$^'))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(*buttons)
    await call.message.edit_text(text=replytext, reply_markup=keyboard, parse_mode='HTML')
    

def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(event_get_all, commands='event')
    dp.register_callback_query_handler(event_get_all_pages, regexp='^eventPages:*')
    dp.register_message_handler(event_start, commands='event_create')
    dp.register_message_handler(event_cancel, state=[FSMEvent.date,FSMEvent.name, FSMEvent.delete], commands='event_cancel')
    dp.register_message_handler(event_set_date, state=FSMEvent.name)
    dp.register_message_handler(event_delete_start, commands='event_delete')
    dp.register_message_handler(event_delete_end, state=FSMEvent.delete)
    dp.register_message_handler(event_end, state=FSMEvent.date)
    dp.register_message_handler(event_add_players, state=FSMEvent.addplayers, regexp='\+')
    dp.register_message_handler(admin_end, state=FSMEvent.admin, commands='event_end')
    dp.register_message_handler(admin_kick, state=FSMEvent.admin, commands='event_kick')
    
    
