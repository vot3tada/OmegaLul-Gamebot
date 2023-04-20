import os
import random
from aiogram.dispatcher import Dispatcher
from aiogram import types
import Classes.Player as Player
import handlers.achievement as AchievementHandler
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

async def getAvatar(message : types.Message):
    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Нужно зарегаться для такого')
        return
    player = Player.GetPlayer(message.chat.id, message.from_user.id)
    orig = player.photo
    level = player.level
    text = f'''
Имя: {player.name}
ХП: {player.hp}
Уровень: {level} 
Опыт: {player.exp}   (x{player.expMultiply})
Деньги: {player.money}
Урон: {player.damage}   (+{round(Player.levelDamageFactor*level)})   (x{player.damageMultiply})
Удача: {player.luck}   (+{round(Player.levelLuckFactor*level,3)})   (x{player.luckMultiply})
Статус:\n'''
    for st in player.GetStatus():
        text += f'{st.name}: {st.description}\n'
    photo=open(orig, "rb")
    await message.answer_photo(photo, caption=text)


async def getInventory(message : types.Message):
    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Нужно зарегаться для такого')
        return
    player = Player.GetPlayer(message.chat.id, message.from_user.id)
    text = 'Ваш инвентарь:'
    photo = open(ROOT / 'static/inventory/' / random.choice(os.listdir(ROOT / 'static/inventory')) ,'rb')
    if len(player.inventory) == 0:
        text += '\nВ данный момент пустует...'
        await message.reply_photo(photo=photo,caption=text)
        return
    keyboard = types.InlineKeyboardMarkup()
    for i in player.inventory:
        keyboard.add(types.InlineKeyboardButton(text = f'{i[0].name}: {i[1]}', callback_data=f"item:{i[0].id}"))
    await message.reply_photo(photo=photo,caption=text, reply_markup=keyboard)

async def getMoney(message: types.Message):
    player = Player.GetPlayer(message.chat.id, message.from_user.id)
    player.money+=2000
    await AchievementHandler.AddHistory(chatId = message.chat.id, userId = message.from_user.id, totalMoney=2000)

def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(getInventory, commands='inventory', state=None)
    dp.register_message_handler(getAvatar, commands='avatar', state=None)
    dp.register_message_handler(getMoney, commands='tyanki_and_grechka', state=None)