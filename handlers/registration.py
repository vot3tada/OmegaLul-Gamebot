from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import utils.avatarCreator as ac
import Classes.Player as Player

class FSMRegistation(StatesGroup):
    name = State()
    changeName = State()
    changePhoto = State()
    photoClass = State()
    photoSend = State()
    acceptPhoto = State()

async def regStart(message : types.Message):
    if Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Ты уже зареган(а)')
        return
    await FSMRegistation.name.set()
    await message.reply('Напиши имя')

async def changeNameStart(message : types.Message):
    if Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Ты ещё не зареган(а)')
        return
    await FSMRegistation.changeName.set()
    await message.reply('Напиши имя')

async def changeNameEnd(message : types.Message, state: FSMContext):
    Player.GetPlayer(message.chat.id, message.from_user.id).name = message.text
    await state.finish()

async def getName(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMRegistation.photoClass.set()
    keyboard = types.InlineKeyboardMarkup()
    for i in ac.classes.keys():
        keyboard.add(types.InlineKeyboardButton(text = i, callback_data=f"class:{i}"))
    await message.reply('Выбери пол:', reply_markup=keyboard)
    
async def changePhoto(message : types.Message):
    await FSMRegistation.photoClass.set()
    text = '\n'
    for i in ac.classes.keys():
        text += i + '\n'
    await message.reply('Выбери пол:' + text)

async def getPhotoclass(call: types.CallbackQuery, state : FSMContext):
    try:
        photoClass = call.data.replace("class:",'')
        async with state.proxy() as data:
            data['photoclass'] = photoClass.lower()
        await FSMRegistation.photoSend.set()
        await call.message.reply('Добавь фото')
    except:
        await call.answer('Неправильный класс фото')    

async def getPhoto(message : types.Message, state: FSMContext):
    orig = f'./static/user/{message.chat.id}_{message.from_user.id}.jpg'
    await message.photo[-1].download(orig)
    try:
        ac.getAvatar(message.chat.id, message.from_user.id, (await state.get_data())['photoclass'])
    except:
        await message.reply('Плохое фото, попробуй ещё раз')
        return
    photo=open(f'./static/player/{message.chat.id}_{message.from_user.id}.jpg', "rb")
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text = 'Беру!', callback_data=f"ava1:{message.chat.id}_{message.from_user.id}"))
    keyboard.add(types.InlineKeyboardButton(text = 'Давай другую...', callback_data=f"ava0:{message.chat.id}_{message.from_user.id}"))
    await FSMRegistation.acceptPhoto.set()
    await message.answer_photo(photo, caption='Как тебе этот облик ?', reply_markup=keyboard)

async def getAnotherPhoto(call: types.CallbackQuery, state: FSMContext):

    chat, user = call.data.replace("ava0:",'').split('_')

    if str(call.from_user.id) != user and str(call.message.chat) != chat:
        await call.answer("Это не ваша личико...")
        return

    ac.getAvatar(call.message.chat.id, call.from_user.id, (await state.get_data())['photoclass'])

    photo=open(f'./static/player/{call.message.chat.id}_{call.from_user.id}.jpg', "rb")
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text = 'Беру!', callback_data=f"ava1:{call.message.chat.id}_{call.from_user.id}"))
    keyboard.add(types.InlineKeyboardButton(text = 'Давай другую...', callback_data=f"ava0:{call.message.chat.id}_{call.from_user.id}"))
    
    await call.message.answer_photo(photo, caption='А этот как ?', reply_markup=keyboard)

async def endRegistation(call: types.CallbackQuery, state: FSMContext):

    chat, user = call.data.replace("ava1:",'').split('_')

    if str(call.from_user.id) != user and str(call.message.chat) != chat:
        await call.answer("Это не ваша личико...")
        return
    
    orig = f'./static/player/{call.message.chat.id}_{call.from_user.id}.jpg'
    photo=open(orig, "rb")
    newPlayer = Player.Player(
        {
            'chatId':call.message.chat.id,
            'userId':call.from_user.id,
        },
        (await state.get_data())['name'],
        orig
    )
    await state.finish()
    Player.AddPlayer(newPlayer)
    await call.message.answer_photo(photo, caption=f'Ещё один красавчик/красавица с нами: {newPlayer.name} !!')


async def cancelRegistration(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Регистрация отменена')
    
def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(regStart, commands='registration', state=None)
    dp.register_message_handler(cancelRegistration, commands='cancel', state=[FSMRegistation.name, FSMRegistation.photoClass, FSMRegistation.photoSend, FSMRegistation.acceptPhoto])
    dp.register_message_handler(getName, state=FSMRegistation.name)
    dp.register_callback_query_handler(getPhotoclass, state=FSMRegistation.photoClass, regexp='^class:*')
    dp.register_message_handler(getPhoto, content_types=['photo'], state=FSMRegistation.photoSend)
    dp.register_callback_query_handler(getAnotherPhoto, regexp="ava0:*", state=FSMRegistation.acceptPhoto)
    dp.register_callback_query_handler(endRegistation, regexp="ava1:*", state=FSMRegistation.acceptPhoto)
    
    