from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import handlers
import Classes


#keyboard = types.InlineKeyboardMarkup()
#keyboard.add(types.InlineKeyboardButton(text="Драться яростно", callback_data=f"fightR:{fights[index][0]}_{fights[index][1]}"))
#keyboard.add(types.InlineKeyboardButton(text="Драться ловко", callback_data=f"fightD:{fights[index][0]}_{fights[index][1]}"))




class FSMShop(StatesGroup):
    isShopping = State()
    goods = [Classes.HPPotion(),
             Classes.DamagePotion(),
             Classes.LuckPotion()]

async def shop_start(message : types.message):
    from .registration import users
    if str(message.from_user.id) not in users.keys():
        await message.reply('Зарегайся другалек')
        return
    #await FSMShop.isShopping.set()
    text = 'Добро пожаловать в магазин!\nУ нас есть:'
    keyboard = types.InlineKeyboardMarkup()
    for i in FSMShop.goods:
        keyboard.add(types.InlineKeyboardButton(text = f'{i.name} - {i.price}', callback_data=f"buy:{i.name}"))
    #keyboard.add(types.InlineKeyboardButton(text = 'Выйти', callback_data=f"buy:Exit"))
    await message.reply(text, reply_markup=keyboard)

async def shopping(message: types.Message, state: FSMContext):
    from .registration import users
    good = 0
    try:
        good = int(message.text)
    except:
        await message.reply('Вводи цифры, черт!')
        return
    if good == 0:
        await state.finish()
        await message.reply('Вы вышли из магазина')
        return
    if good > len(FSMShop.goods) or good < 1:
        await message.reply('У нас нет такого товара')
        return
    users[str(message.from_user.id)].inventory.append(FSMShop.goods[good-1])
    await message.reply('Товар успешно куплен')



async def shopp(call: types.CallbackQuery, state : FSMContext):
    try:
        from .registration import users
        buy = call.data.replace("buy:",'')
        #if buy == 'Exit':
        #    await state.finish()
        #    await call.message.answer('Вы вышли из магазина')
        #    return
        good = [i for i in FSMShop.goods if i.name == buy][0]
        if users[str(call.from_user.id)].money < good.price:
            await call.answer('У вас не хватает денег')
            return
        users[str(call.from_user.id)].money -= good.price
        users[str(call.from_user.id)].inventory.append(good)
        await call.answer('Вы купили')
        await call.answer()
    except:
        state.finish()
    

def register_handlers_shop(dp: Dispatcher):
    dp.register_message_handler(shop_start, regexp='^Магазин$', state=None)
    dp.register_callback_query_handler(shopp, regexp='^buy:*')

