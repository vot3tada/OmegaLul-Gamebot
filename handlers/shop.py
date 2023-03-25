from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import handlers
import Classes

users = handlers.registration.users

class FSMShop(StatesGroup):
    isShopping = State()
    goods = ['Хилка - восполнить хп', 
             'Бустер exp - увеличивает получение опыта в 2 раза на 24 часа',
             'Сиги - дает 5 минут отдыха',
             'НУЖНО НАПИСАТЬ НОРМАЛЬНЫЙ КЛАСС ПРЕДМЕТОВ И ИХ СВОЙСТВ']

async def shop_start(message : types.Message):
    if str(message.from_user.id) not in users.keys():
        await message.reply('Зарегайся другалек')
        return
    await FSMShop.isShopping.set()
    text = 'Добро пожаловать в магазин!\nУ нас есть:'
    for i in range(0, len(FSMShop.goods)):
        text += f'\n{i+1}. {FSMShop.goods[i]}'
    text += '\n0. Выйти из магазина'
    await message.reply(text)

async def shopping(message: types.Message, state: FSMContext):
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

def register_handlers_shop(dp: Dispatcher):
    dp.register_message_handler(shop_start, regexp='^Магазин$', state=None)
    dp.register_message_handler(shopping, state=FSMShop.isShopping)

