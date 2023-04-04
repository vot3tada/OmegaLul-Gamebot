from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import Classes.Player as Player

async def get_avatar(message : types.Message, state: FSMContext):
    if not Player.FindPlayer(f'{message.chat.id}_{message.from_user.id}'):
        await message.reply('Нужно зарегаться для такого')
        return
    player = Player.GetPlayer(f'{message.chat.id}_{message.from_user.id}')
    orig = player.photo
    text = f'Имя: {player.name}\nХП: {player.hp}\nОпыт: {player.exp}\nДеньги: {player.money}\nСтатус:\n'
    for st in player.status:
        text += f'{st.name}: {st.description}\n'
    photo=open(orig, "rb")
    await message.answer_photo(photo, caption=text)


async def get_inventory(message : types.Message):
    if not Player.FindPlayer(f'{message.chat.id}_{message.from_user.id}'):
        await message.reply('Нужно зарегаться для такого')
        return
    player = Player.GetPlayer(f'{message.chat.id}_{message.from_user.id}')
    text = 'Ваш инвентарь:'
    if len(player.inventory) == 0:
        text += '\nОй, ваш инвентарь пуст😢'
        await message.reply(text)
        return
    keyboard = types.InlineKeyboardMarkup()
    for i in player.inventory:
        keyboard.add(types.InlineKeyboardButton(text = f'{i[0].name}: {player.inventory.count(i)}', callback_data=f"item:{i[0].id}"))
    await message.reply(text, reply_markup=keyboard)

def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(get_inventory, regexp='^Инвентарь$', state=None)
    dp.register_message_handler(get_avatar, regexp='^Аватар$', state=None)