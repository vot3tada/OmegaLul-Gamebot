from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import Classes.Event as Event
from datetime import datetime, date, time
from utils.scheduler import scheduler
import Classes.Player as Player
from utils.create_bot import bot, dp
import random
import os

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
    await message.answer('Создание отменено')

async def event_delete_start(message : types.Message, state: FSMContext):
    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Нужно зарегаться для такого')
        return
    await FSMEvent.delete.set()
    await message.answer('Напишите номер эвента')

async def event_delete_end(message : types.Message, state: FSMContext):
    event = Event.GetEvent(message.text)
    if (event == None):
        await message.answer('Такого эвента не существует')
        return
    player : Player.Player = Player.GetPlayer(message.chat.id, message.from_user.id)
    if (event.creator.chatId != player.chatId or event.creator.userId != player.userId):
        await message.answer('Вы не являетесь создателем этого эвента')
        return
    scheduler.remove_job('e'+event.id+'-')
    scheduler.remove_job('e'+event.id+'--')
    state.finish()
    await message.answer('Эвент отменен')
    

async def event_end(message : types.Message, state: FSMContext):
    from dateutil import tz
    event = Event.Event()
    async with state.proxy() as data:
        event.name = data['name']
    date = message.text.split('/')
    try:
        event.datetime = datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]), tzinfo=tz.gettz("Europe/Moscow"))
    except:
        await message.reply('Неправильный формат даты: ГГГГ/ММ/ДД/ЧЧ/ММ')
        return
    if len([i for i in Event.GetAllEvents() if abs((event.datetime-i.datetime).total_seconds()) < 600]) > 0:
        await message.reply('В это время уже существует эвент')
        return
    event.creator = Player.GetPlayer(message.chat.id, message.from_user.id)
    event.id = str(Event.GetCount())
    Event.AddEvent(event)
    await state.finish()
    await message.reply(f'Мероприятие с #{event.id} создано')
    photo = open('./static/anonce/' + random.choice(os.listdir('./static/anonce')) ,'rb')

    await bot.send_photo(chat_id=message.chat.id,  
                        caption=f'<b>ВСЕ! ВСЕ! ВСЕ!</b>\nУслышьте! Этого числа <b>{event.datetime:%d.%m.%Y}</b> ' +
                        f'в <b>{event.datetime:%H:%M}</b> состоится эвент:\n<b>{event.name}</b>!\n' +
                        'Не опаздывайте! Награда ждет посетителей!', 
                        photo=photo,
                        parse_mode='HTML')
    scheduler.add_job(trigger_before_event, 'date', run_date= 
                      datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]) - 1, int(date[4]), 
                                                                        tzinfo=tz.gettz("Europe/Moscow")), args=[message.chat.id, event.name], id=('e'+str(event.id)+'-'))
    scheduler.add_job(trigger_event, 'date', run_date= datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]), 
                                                                        tzinfo=tz.gettz("Europe/Moscow")), args=[message.chat.id, event.id], id=('e'+str(event.id)+'--'))

async def trigger_before_event(chatId: int, eventName: str):
    await bot.send_message(chat_id=chatId, text=f'Через час пройдет эвент: \n<b>{eventName}</b>.\n Будет награда.', parse_mode='HTML')

async def trigger_event(chatId: int, eventId: int):
    event = Event.GetEvent(eventId)
    photo = open('./static/meeting/' + random.choice(os.listdir('./static/meeting')) ,'rb')
    await bot.send_photo(chat_id=chatId,  
                            caption=f'Сейчас проходит эвент:\n<b>{event.name}</b>.\nУ вас есть пять минут проставить плюсики. Всем посетителям награда!', 
                            photo=photo,
                            parse_mode='HTML')
    for i in Player.GetAllPlayers(chatId):
        st : FSMContext = dp.current_state(chat = i.chatId, user = i.userId)
        statePlayer = await st.get_state()
        if statePlayer == None:
            await st.set_state(FSMEvent.addplayers)
            await st.set_data(event.id)
    st : FSMContext = dp.current_state(chat = event.creator.chatId, user = event.creator.userId)
    await st.set_state(FSMEvent.admin)
    await st.set_data(event.id)
    scheduler.add_job(event_set_state, trigger='interval', seconds=2, jobstore='local', args=[event.creator.chatId, eventId], coalesce=True, id=f'event:{eventId}reload')
    scheduler.add_job(scheduler_end, trigger='interval', seconds=300, jobstore='local', args=[event.creator.chatId, eventId], coalesce=True, id=f'event:{eventId}end')

async def event_add_players(message : types.Message, state: FSMContext):
    eventId = await state.get_data()
    event = Event.GetEvent(eventId)
    player: Player.Player = Player.GetPlayer(message.chat.id, message.from_user.id)
    event.players.append(player)
    await message.reply(f'{player.name} подключился')
    await FSMEvent.inEvent.set()

async def admin_end(message : types.Message, state: FSMContext):
    for i in Player.GetAllPlayers(message.chat.id):
        st : FSMContext = dp.current_state(chat = i.chatId, user = i.userId)
        statePlayer = await st.get_state()
        if statePlayer == FSMEvent.addplayers or statePlayer == FSMEvent.inEvent:
            await dp.current_state(chat = i.chatId, user = i.userId).set_state(None)
    eventId = await state.get_data()
    event = Event.GetEvent(eventId)
    text = 'Посетители эвента:'
    for i in event.players:
        i.money += 50
        i.exp += 50
        text += f'\n {i.name}'
    await message.answer('Регистрация на эвент завершена\n' + text + '\nКаждый посетитель получил:\n50 опыта\n50 монет')
    scheduler.remove_job(f'event:{eventId}end')
    scheduler.remove_job(f'event:{eventId}reload')
    await state.finish()

async def scheduler_end(chatId: int, eventId):
    for i in Player.GetAllPlayers(chatId):
        st : FSMContext = dp.current_state(chat = i.chatId, user = i.userId)
        statePlayer = await st.get_state()
        if statePlayer == FSMEvent.addplayers or statePlayer == FSMEvent.inEvent or FSMEvent.admin:
            await dp.current_state(chat = i.chatId, user = i.userId).set_state(None)
    event = Event.GetEvent(eventId)
    text = 'Посетители эвента:'
    for i in event.players:
        i.money += 50
        i.exp += 50
        text += f'\n {i.name}'
    await bot.send_message(chat_id=chatId, text='Регистрация на эвент завершена\n' + text + '\nКаждый посетитель получил:\n50 опыта\n50 монет')
    scheduler.remove_job(f'event:{eventId}end')
    scheduler.remove_job(f'event:{eventId}reload')

async def admin_kick(message : types.Message, state: FSMContext):
    eventId = await state.get_data()
    event = Event.GetEvent(eventId)
    if not message.reply_to_message is None:
        eventUserId = [i.userId for i in event.players]
        if message.reply_to_message.from_user.id in eventUserId:
            event.players.pop(eventUserId.index(message.reply_to_message.from_user.id))
            await message.reply(f'Выписан из движа')
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


     
     




def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(event_start, commands='event_create')
    dp.register_message_handler(event_cancel, state=[FSMEvent.date,FSMEvent.name, FSMEvent.delete], commands='event_cancel')
    dp.register_message_handler(event_set_date, state=FSMEvent.name)
    dp.register_message_handler(event_delete_start, commands='event_delete')
    dp.register_message_handler(event_delete_end, state=FSMEvent.delete)
    dp.register_message_handler(event_end, state=FSMEvent.date)
    dp.register_message_handler(event_add_players, state=FSMEvent.addplayers, regexp='\+')
    dp.register_message_handler(admin_end, state=FSMEvent.admin, commands='event_end')
    dp.register_message_handler(admin_kick, state=FSMEvent.admin, commands='event_kick')
    
    
