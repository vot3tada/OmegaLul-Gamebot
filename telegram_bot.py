from aiogram.utils import executor
from create_bot import dp
import handlers

handlers.register_handlers(dp)

executor.start_polling(dp, skip_updates=True)

"""@dp.message_handler(commands='Аватар')
async def login_start(message: types.Message, state: FSMContext):
    
    await state.set_state(Login)
    await message.answer

@dp.message_handler(commands='Эхо')
async def echo_start(message : types.Message, state: FSMContext):
    await message.answer('Папугай включен')
    #async with state.proxy() as data:
    #    data['name'] = 'play'
    chats[str(message.chat.id)] = 'echo'
    print(chats)


@dp.message_handler(commands='ЭхоОфф')
async def echo_end(message : types.Message, state: FSMContext):
    await message.answer('Папугай выключен')
    #await state.finish()
    chats[str(message.chat.id)] = None


@dp.message_handler(content_types=['photo'])
async def get_image(message : types.Message):
    orig = f'./static/{message.from_user.id}.jpg'
    await message.photo[-1].download(orig)
    ac.getAvatar(orig)
    await message.answer('Фото загружено')

@dp.message_handler(commands='Get')
async def get_image(message : types.Message, state: FSMContext):
    orig = f'./static/{message.from_user.id}.jpg'
    photo=open(orig, "rb")
    if photo:
        await message.answer_photo(photo)
        await state.finish()
    else:
        await message.answer('Нет изображения')

@dp.message_handler()
async def echo_send(message : types.Message):
    #async with state.proxy() as data:
        #if data and data['name'] == 'play':
    print(f'Ебанат натрия {message.chat.id}')
    if str(message.chat.id) in chats and chats[str(message.chat.id)]:
        await message.answer(message.from_user.first_name +': '+message.text)"""

executor.start_polling(dp, skip_updates = True)