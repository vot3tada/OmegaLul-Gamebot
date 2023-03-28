from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from Classes.events import Event
from datetime import datetime, date, time

class FSMEvent(StatesGroup):
    name = State()
    date = State()
    addplayers = State()

async def event_start(message : types.message):
    await FSMEvent.name.set()
    await message.reply('Напишите название мероприятия')

async def event_set_date(message : types.message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMEvent.date.set()
    await message.reply('Напишите дату и время мероприятия в формате: ГГГГ/ММ/ДД/ЧЧ/ММ ')

async def event_end(message : types.message, state: FSMContext):
    try:
        event = Event()
        async with state.proxy() as data:
            event.name = data['name']
        await state.finish()
        date = message.text.split('/')
        event.datetime = datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]))
        await message.reply('Мероприятие создано')
        await message.answer(f'ВСЕ! ВСЕ! ВСЕ!\nУслышьте! Этого числа {event.datetime:%d.%m.%Y} ' +
                            f'в {event.datetime:%H:%M} состоится эвент: {event.name}! ' +
                            'Не опаздывайте!')
    except:
        await message.reply('ДАТА В ФОРМАТЕ: ГГГГ/ММ/ДД/ЧЧ/ММ')

def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(event_start, regexp='^Создать эвент$')
    dp.register_message_handler(event_set_date, state=FSMEvent.name)
    dp.register_message_handler(event_end, state=FSMEvent.date)
    
