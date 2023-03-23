from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from create_bot import dp, bot
from bot_telegram import users
import avatarCreator as ac

class FSMRegistation(StatesGroup):
    name = State()
    photo = State()
    #health = State()
    #Exp = State()
    #Money = State()


#@dp.message_handler(commands='Регистрация')
async def reg_start(message : types.Message):
    await FSMRegistation.name.set()
    await message.reply('Напиши имя')

#@dp.message_handler(state=FSMRegistation.name)
async def get_name(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMRegistation.photo.set()
    await message.reply('Добавь фото')

#@dp.message_handler(content_types=['photo'], state=FSMRegistation.photo)
async def end_registation(message : types.Message, state: FSMContext):
    orig = f'./static/{message.from_user.id}.jpg'
    await message.photo[-1].download(orig)
    try:
        ac.getAvatar(orig)
    except:
        await message.reply('Плохое фото, попробуй ещё раз')
    async with state.proxy() as data:
        users[str(message.from_user.id)] = data['name'] 
    await state.reset_state(with_data=False)
    await message.reply('Регистрация завершена')
    

#@dp.message_handler(commands='Аватар')
async def get_avatar(message : types, state: FSMContext):
    orig = f'./static/{message.from_user.id}.jpg'
    photo=open(orig, "rb")
    text = ''
    async with state.proxy() as data:
        text = data['name']
    await message.answer_photo(photo, caption=text)
    


def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(reg_start, commands=['Регистрация'], state=None)
    dp.register_message_handler(get_avatar, commands=['Аватар'], state=None)
    dp.register_message_handler(get_name, state=FSMRegistation.name)
    dp.register_message_handler(end_registation, state=FSMRegistation.photo)
    