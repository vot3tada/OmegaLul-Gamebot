from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from Classes.Player import Players

async def get_avatar(message : types, state: FSMContext):
    if not f'{message.chat.id}_{message.from_user.id}'  in Players.keys():
        await message.reply('Нужно зарегаться для такого')
        return
    player = Players[f'{message.chat.id}_{message.from_user.id}']
    orig = player.photo
    text = f'Имя: {player.name}\nХП: {player.hp}\nОпыт: {player.exp}\nДеньги: {player.money}'
    photo=open(orig, "rb")
    await message.answer_photo(photo, caption=text)


async def get_inventory(message : types):
    if not f'{message.chat.id}_{message.from_user.id}' in Players.keys():
        await message.reply('Нужно зарегаться для такого')
        return
    player = Players[f'{message.chat.id}_{message.from_user.id}']
    text = 'Ваш инвентарь:'
    if len(player.inventory) == 0:
        text += '\nОй, ваш инвентарь пуст😢'
        await message.reply(text)
        return
    keyboard = types.InlineKeyboardMarkup()
    setInventory = set(player.inventory)
    for i in setInventory:
        keyboard.add(types.InlineKeyboardButton(text = f'{i.name}: {player.inventory.count(i)}', callback_data=f"use:{i.name}"))
    await message.reply(text, reply_markup=keyboard)

def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(get_inventory, regexp='^Инвентарь$', state=None)
    dp.register_message_handler(get_avatar, regexp='^Аватар$', state=None)