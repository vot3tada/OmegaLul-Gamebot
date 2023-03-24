from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import avatarCreator as ac

users = dict()

class FSMRegistation(StatesGroup):
    name = State()
    photo = State()

async def reg_start(message : types.Message):
    await FSMRegistation.name.set()
    await message.reply('Напиши имя')

async def get_name(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMRegistation.photo.set()
    await message.reply('Добавь фото')

async def end_registation(message : types.Message, state: FSMContext):
    orig = f'./static/{message.from_user.id}.jpg'
    await message.photo[-1].download(orig)
    try:
        ac.getAvatar(orig)
    except:
        await message.reply('Плохое фото, попробуй ещё раз')
        return
    async with state.proxy() as data:
        users[str(message.from_user.id)] = data['name'] 
    await state.reset_state(with_data=False)
    await message.reply('Регистрация завершена')

async def get_avatar(message : types, state: FSMContext):
    orig = f'./static/{message.from_user.id}.jpg'
    photo=open(orig, "rb")
    text = ''
    async with state.proxy() as data:
        text = data['name']
    await message.answer_photo(photo, caption=text)
    
def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(reg_start, regexp='^Регистрация$', state=None)
    dp.register_message_handler(get_avatar, regexp='^Аватар$', state=None)
    dp.register_message_handler(get_name, state=FSMRegistation.name)
    dp.register_message_handler(end_registation, content_types=['photo'], state=FSMRegistation.photo)
    