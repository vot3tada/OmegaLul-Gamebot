from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import utils.avatarCreator as ac
import Classes.Item as Item
from Classes.Player import Players, Player

class FSMRegistation(StatesGroup):
    name = State()
    change_name = State()
    change_photo = State()
    photoclass = State()
    photo = State()

async def reg_start(message : types.Message):
    if f'{message.chat.id}_{message.from_user.id}' in Players.keys():
        await message.reply('Ты уже зареган(а)')
        return
    await FSMRegistation.name.set()
    await message.reply('Напиши имя')

async def change_name_start(message : types.Message):
    #Проверочку бы...
    await FSMRegistation.change_name.set()
    await message.reply('Напиши имя')

async def change_name_end(message : types.Message, state: FSMContext):
    Players[str(message.from_user.id)] = message.text
    await state.finish()

async def get_name(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMRegistation.photoclass.set()
    keyboard = types.InlineKeyboardMarkup()
    for i in ac.classes.keys():
        keyboard.add(types.InlineKeyboardButton(text = i, callback_data=f"class:{i}"))
    await message.reply('Выбери класс фото:', reply_markup=keyboard)


    
async def change_photo(message : types.Message):
    await FSMRegistation.photoclass.set()
    text = '\n'
    for i in ac.classes.keys():
        text += i + '\n'
    await message.reply('Выбери класс фото:' + text)

async def get_photoclass(call: types.CallbackQuery, state : FSMContext):
    try:
        photoClass = call.data.replace("class:",'')
        async with state.proxy() as data:
            data['photoclass'] = photoClass.lower()
            print(photoClass)
        await FSMRegistation.photo.set()
        await call.message.reply('Добавь фото')
    except:
        await call.answer('Неправильный класс')    


async def end_registation(message : types.Message, state: FSMContext):
    orig = f'./static/{message.chat.id}_{message.from_user.id}.jpg'
    await message.photo[-1].download(orig)
    try:
        ac.getAvatar(orig, (await state.get_data())['photoclass'])
    except:
        await message.reply('Плохое фото, попробуй ещё раз')
        return
    newPlayer = Player()
    async with state.proxy() as data:
        newPlayer.name = data['name']
    await state.finish()
    newPlayer.photo = orig
    Players[f'{message.chat.id}_{message.from_user.id}'] = newPlayer 
    photo=open(orig, "rb")
    
    await message.answer_photo(photo, caption='Ещё один красавчик/одна чикуля с нами: ' + Players[f'{message.chat.id}_{message.from_user.id}'].name + '!!')


async def cancel_registration(message: types, state: FSMContext):
    await state.finish()
    await message.reply('Регистрация отменена')
    
def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(reg_start, regexp='^Регистрация$', state=None)
    dp.register_message_handler(cancel_registration, regexp='^Отмена$', state=[FSMRegistation.name,FSMRegistation.photoclass, FSMRegistation.photo])
    dp.register_message_handler(get_name, state=FSMRegistation.name)
    dp.register_callback_query_handler(get_photoclass, state=FSMRegistation.photoclass, regexp='^class:*')
    dp.register_message_handler(end_registation, content_types=['photo'], state=FSMRegistation.photo)
    
    