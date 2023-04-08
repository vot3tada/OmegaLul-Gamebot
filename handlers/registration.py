from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import utils.avatarCreator as ac
import Classes.Player as Player

class FSMRegistation(StatesGroup):
    name = State()
    change_name = State()
    change_photo = State()
    photoclass = State()
    photo = State()

async def reg_start(message : types.Message):
    if Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Ты уже зареган(а)')
        return
    await FSMRegistation.name.set()
    await message.reply('Напиши имя')

async def change_name_start(message : types.Message):
    if Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Ты ещё не зареган(а)')
        return
    await FSMRegistation.change_name.set()
    await message.reply('Напиши имя')

async def change_name_end(message : types.Message, state: FSMContext):
    Player.GetPlayer(message.chat.id, message.from_user.id).name = message.text
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
    newPlayer = Player.Player(
        {
            'chatId':message.chat.id,
            'userId':message.from_user.id,
        },
        (await state.get_data())['name'],
        orig
    )
    await state.finish()
    Player.AddPlayer(newPlayer)
    photo=open(orig, "rb")
    await message.answer_photo(photo, caption='Ещё один красавчик/одна чикуля с нами: ' + newPlayer.name + '!!')


async def cancel_registration(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Регистрация отменена')
    
def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(reg_start, commands='registration', state=None)
    dp.register_message_handler(cancel_registration, commands='cancel', state=[FSMRegistation.name, FSMRegistation.photo])
    dp.register_message_handler(get_name, state=FSMRegistation.name)
    dp.register_callback_query_handler(get_photoclass, state=FSMRegistation.photoclass, regexp='^class:*')
    dp.register_message_handler(end_registation, content_types=['photo'], state=FSMRegistation.photo)
    
    