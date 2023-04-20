from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import Classes.Player as Player
import Classes.Good as Good
import random
import os
import handlers.achievement as AchievementHandler
from pathlib import Path
from utils import ParseSeconds

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

class FSMShop(StatesGroup):
    isShopping = State()

async def shop_start(message : types.Message):
    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Нужно зарегаться для такого')
        return

    text = 'Добро пожаловать в магазин!\nУ нас есть:\n'
    keyboard = types.InlineKeyboardMarkup()
    Items = Good.GetClassItem('shop')
    for i in Items:
        text+=f'''<b>{i.name}</b>   
Цена: {i.price} монет
{i.description}
Длительность: {ParseSeconds(i.duration)}

'''
        keyboard.add(types.InlineKeyboardButton(text = f'Купить  {i.name}', callback_data=f"buy:{i.id}"))

    await message.reply_photo(
        photo= open(ROOT / 'static/shop/' / random.choice(os.listdir(ROOT / 'static/shop')) ,'rb'),
        caption=text, 
        reply_markup=keyboard,
        parse_mode='HTML')

async def shopping(call: types.CallbackQuery, state : FSMContext):
    if not Player.FindPlayer(call.message.chat.id, call.from_user.id):
        await call.answer('Нужно зарегаться для такого')
        return
    """try:"""
    try:
        id = int(call.data.replace("buy:",''))
    except:
        call.answer('id предмета не определен')
    #if buy == 'Exit':
    #    await state.finish()
    #    await call.message.answer('Вы вышли из магазина')
    #    return
    good = Good.GetItem(id)
    player = Player.GetPlayer(call.message.chat.id, call.from_user.id)
    if player.money < good.price:
        await call.answer('У вас не хватает денег')
        return
    player.money -= good.price
    player.AddItem(good)
    await AchievementHandler.AddHistory(chatId = player.chatId, userId = player.userId, totalItem=1)
    await call.answer('Вы купили')
    """except:
        await state.finish()
        await call.answer()"""

def register_handlers_shop(dp: Dispatcher):
    dp.register_message_handler(shop_start, commands='shop', state=None)
    dp.register_callback_query_handler(shopping, regexp='^buy:*')

