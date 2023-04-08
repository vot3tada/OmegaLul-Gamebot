import os
import random
from aiogram.dispatcher import Dispatcher
from aiogram import types
import Classes.Player as Player

async def getAvatar(message : types.Message):
    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Нужно зарегаться для такого')
        return
    player = Player.GetPlayer(message.chat.id, message.from_user.id)
    orig = player.photo
    text = f'Имя: {player.name}\nХП: {player.hp}\nУровень: {player.level} (опыт: {player.exp})\nДеньги: {player.money}\nСтатус:\n'
    for st in player.status:
        text += f'{st.name}: {st.description}\n'
    photo=open(orig, "rb")
    await message.answer_photo(photo, caption=text)


async def getInventory(message : types.Message):
    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Нужно зарегаться для такого')
        return
    player = Player.GetPlayer(message.chat.id, message.from_user.id)
    text = 'Ваш инвентарь:'
    photo = open('./static/inventory/' + random.choice(os.listdir('./static/inventory')) ,'rb')
    if len(player.inventory) == 0:
        text += '\nВ данный момент пустует...'
        await message.reply_photo(photo=photo,caption=text)
        return
    keyboard = types.InlineKeyboardMarkup()
    for i in player.inventory:
        keyboard.add(types.InlineKeyboardButton(text = f'{i[0].name}: {i[1]}', callback_data=f"item:{i[0].id}"))
    await message.reply_photo(photo=photo,caption=text, reply_markup=keyboard)

def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(getInventory, commands='inventory', state=None)
    dp.register_message_handler(getAvatar, commands='avatar', state=None)