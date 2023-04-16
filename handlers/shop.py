from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import Classes.Player as Player
import Classes.Good as Good
import random
import os

#keyboard = types.InlineKeyboardMarkup()
#keyboard.add(types.InlineKeyboardButton(text="Драться яростно", callback_data=f"fightR:{fights[index][0]}_{fights[index][1]}"))
#keyboard.add(types.InlineKeyboardButton(text="Драться ловко", callback_data=f"fightD:{fights[index][0]}_{fights[index][1]}"))

class FSMShop(StatesGroup):
    isShopping = State()

async def shop_start(message : types.Message):
    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Нужно зарегаться для такого')
        return

    text = 'Добро пожаловать в магазин!\nУ нас есть:\n'
    keyboard = types.InlineKeyboardMarkup()
    Items = Good.GetAllItems()
    for i in Items:
        time = ''
        if i.duration // 86400:
            time += f'{i.duration // 86400} д. '
        if  (i.duration % 86400)// 3600:
            time += f'{(i.duration % 86400)// 3600} ч. '
        if (i.duration % 3600)// 60:
            time += f'{(i.duration % 3600)// 60} м. '
        text+=f'''
        <b>{i.name}</b>
        {i.description}
        Цена: {i.price} монет
        Длительность: {time}
        '''
        keyboard.add(types.InlineKeyboardButton(text = f'Купить  {i.name}', callback_data=f"buy:{i.id}"))

    await message.reply_photo(
        photo= open('./static/shop/' + random.choice(os.listdir('./static/shop')) ,'rb'),
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
    await call.answer('Вы купили')
    """except:
        await state.finish()
        await call.answer()"""

def register_handlers_shop(dp: Dispatcher):
    dp.register_message_handler(shop_start, commands='shop', state=None)
    dp.register_callback_query_handler(shopping, regexp='^buy:*')

