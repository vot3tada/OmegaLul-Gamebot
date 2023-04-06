from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import Classes.Player as Player
from Classes.Item import Items


#keyboard = types.InlineKeyboardMarkup()
#keyboard.add(types.InlineKeyboardButton(text="Драться яростно", callback_data=f"fightR:{fights[index][0]}_{fights[index][1]}"))
#keyboard.add(types.InlineKeyboardButton(text="Драться ловко", callback_data=f"fightD:{fights[index][0]}_{fights[index][1]}"))

class FSMShop(StatesGroup):
    isShopping = State()

async def shop_start(message : types.Message):
    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Нужно зарегаться для такого')
        return
    #await FSMShop.isShopping.set()
    text = 'Добро пожаловать в магазин!\nУ нас есть:'
    keyboard = types.InlineKeyboardMarkup()
    for i in Items.values():
        keyboard.add(types.InlineKeyboardButton(text = f'{i.name} - {i.price}', callback_data=f"buy:{i.id}"))
    #keyboard.add(types.InlineKeyboardButton(text = 'Выйти', callback_data=f"buy:Exit"))
    await message.reply(text, reply_markup=keyboard)

async def shopping(call: types.CallbackQuery, state : FSMContext):
    if not Player.FindPlayer(call.message.chat.id, call.from_user.id):
        await call.answer('Нужно зарегаться для такого')
        return
    """try:"""
    buy : str = call.data.replace("buy:",'')
    #if buy == 'Exit':
    #    await state.finish()
    #    await call.message.answer('Вы вышли из магазина')
    #    return
    good = Items[buy]
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

