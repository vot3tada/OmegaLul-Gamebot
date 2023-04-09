from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import Classes.Event as Event
from datetime import datetime, date, time
from utils.scheduler import scheduler
import Classes.Player as Player
from utils.create_bot import bot, dp

class FSMEvent(StatesGroup):
    name = State()
    date = State()
    addplayers = State()
    admin = State()

async def event_start(message : types.message):
    await FSMEvent.name.set()
    await message.reply('Напишите название мероприятия')

async def event_set_date(message : types.message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMEvent.date.set()
    await message.reply('Напишите дату и время мероприятия в формате: ГГГГ/ММ/ДД/ЧЧ/ММ')

async def event_end(message : types.message, state: FSMContext):
    from dateutil import tz
    event = Event.Event()
    async with state.proxy() as data:
        event.name = data['name']
    await state.finish()
    date = message.text.split('/')
    try:
        event.datetime = datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]), tzinfo=tz.gettz("Europe/Moscow"))
    except:
        await message.reply('Неправильный формат даты: ГГГГ/ММ/ДД/ЧЧ/ММ')
    event.creator = Player.GetPlayer(message.chat.id, message.from_user.id)
    Event.AddEvent(event)
    await message.reply('Мероприятие создано')
    await message.answer(f'ВСЕ! ВСЕ! ВСЕ!\nУслышьте! Этого числа {event.datetime:%d.%m.%Y} ' +
                        f'в {event.datetime:%H:%M} состоится эвент: {event.name}! ' +
                        'Не опаздывайте! Награда ждет посетителей!')
    scheduler.add_job(trigger_before_event, 'date', run_date= datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]) - 1, int(date[4]), 
                                                                        tzinfo=tz.gettz("Europe/Moscow")), args=[event, message], id=(message.text + str(message.from_user.id)+'0'))
    scheduler.add_job(trigger_event, 'date', run_date= datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]), 
                                                                        tzinfo=tz.gettz("Europe/Moscow")), args=[event, message, state], id=(message.text + str(message.from_user.id)+'1'))

async def trigger_before_event(event: Event, message : types.message):
    await message.answer(f'Через час пройдет эвент: {event.name}. Будет награда.')

async def trigger_event(event: Event, message : types.message, state : FSMContext):
    await message.answer(f'Сейчас проходит эвент: {event.name}. У вас есть минута проставить плюсики. Всем посетителям награда!')
    async with state.proxy() as data:
        data['addplayers'] = event
    for i in Player.GetAllPlayers(message.chat.id):
        st : FSMContext = dp.current_state(chat = i.chatId, user = i.userId)
        statePlayer = await st.get_state()
        if statePlayer == None:
            await st.set_state(FSMEvent.addplayers)
            await st.set_data(event.id)
    st : FSMContext = dp.current_state( chat = event.creator.chatId, user = event.creator.userId)
    await st.set_state(FSMEvent.admin)
    await st.set_data(event.id)
    print()
    

async def event_add_players(message : types.Message, state: FSMContext):
    eventId = await state.get_data()
    event = Event.GetEvent(eventId)
    player: Player = Player.GetPlayer(message.chat.id, message.from_user.id)
    event.players.append(player)
    await message.reply(f'{player.name} подключился')
    await state.finish()

async def admin_end(message : types.message, state: FSMContext):
    for i in Player.GetAllPlayers(message.chat.id):
        st : FSMContext = dp.current_state(chat = i.chatId, user = i.userId)
        statePlayer = await st.get_state()
        if statePlayer == FSMEvent.addplayers:
            await dp.current_state(chat = i.chatId, user = i.userId).set_state(None)
    eventId = await state.get_data()
    event = Event.GetEvent(eventId)
    text = 'Посетители эвента:'
    for i in event.players:
        player : Player = Player.GetPlayer(i.chatId, i.userId)
        player.money += 50
        player.exp += 50
        text += f'\n {i.name}'
    await message.answer('Регистрация на эвент завершена\n' + text + '\nКаждый посетитель получил:\n50 опыта\n50 монет')
    await state.finish()

async def admin_kick(message : types.Message, state: FSMContext):
    eventId = await state.get_data()
    event = Event.GetEvent(eventId)
    if not message.reply_to_message is None:
        player = Player.GetPlayer(message.reply_to_message.chat.id, message.reply_to_message.from_user.id)
        if player in event.players:
            event.players.remove(player)
            await message.reply(f'{player.name} выписан из движа')
        else:
            await message.reply('Такой чел не в эвенте')
    else:
        await message.reply('Вы не выделили человечка')


     
     




def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(event_start, regexp='^Создать эвент$')
    dp.register_message_handler(event_set_date, state=FSMEvent.name)
    dp.register_message_handler(event_end, state=FSMEvent.date)
    dp.register_message_handler(event_add_players, state=FSMEvent.addplayers, regexp='\+')
    dp.register_message_handler(admin_end, state=FSMEvent.admin, regexp='^Закончить$')
    dp.register_message_handler(admin_kick, state=FSMEvent.admin, regexp='^Кик$')
    
    
