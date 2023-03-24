from aiogram import types
from aiogram.dispatcher import Dispatcher

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot

fights = []


class Fight(StatesGroup):
    Ready = State()

def fightsFind(id : int):
    for i in range(len(fights)):
        if fights[i][0] == id or fights[i][1] == id:
            return i
    return -1

async def fight_call(message : types.Message):
    if message.reply_to_message is not None:
        if fightsFind(message.from_user.id) != -1:
            await message.answer('Незя кинуть сразу две перчатки, отмените прошлую дуэль')
            return
        if message.reply_to_message.from_user.id == message.from_user.id:
            await message.answer('Незя дуэлиться с шизой')
            return
        if message.reply_to_message.from_user.id == (await bot.get_me()).id:
            await message.answer('Этот противник вам не по зубам, салага')
            return
        fights.append([message.from_user.id, message.reply_to_message.from_user.id, False])
        await message.answer(f'{message.from_user.full_name} бросил вызов {message.reply_to_message.from_user.id}!')
    else:
        await message.answer(f'С кем дуэль то, {message.from_user.full_name} ?')

async def fight_refuse(message: types.Message, state :FSMContext):
    index = fightsFind(message.from_user.id)
    if index == -1:
        await message.answer("Нечего отменять")
    else:
        st = dp.current_state(chat= message.chat.id, user=fights[index][0])
        if await st.get_state() == 'Fight:Ready':
            await state.finish()
        st = dp.current_state(chat=message.chat.id, user=fights[index][1])
        if await st.get_state() == 'Fight:Ready':
            await state.finish()
        fights.pop(index)
        await message.answer("Дуэль отменена")


async def fight_accept(message: types.Message):
    index = fightsFind(message.from_user.id)
    if index == -1 or fights[index][0] == message.from_user.id:
        await message.answer("Нечего принимать")
    else:
        st : FSMContext = dp.current_state(chat=message.chat.id, user=fights[index][0])
        await st.set_state(Fight.Ready)
        st : FSMContext = dp.current_state(chat=message.chat.id, user=fights[index][1])
        await st.set_state(Fight.Ready)
        fights[index][2] = True
        await message.answer("Дуэль начинается !!!!")

async def attack(message: types.Message):
    await message.answer("Тыщ")



#################################################
def register_fight_handlers(dp : Dispatcher):
    dp.register_message_handler(fight_call, regexp='^Дуэль$')
    dp.register_message_handler(fight_refuse, state=[None,Fight.Ready], regexp='^Отменить дуэль$')
    dp.register_message_handler(fight_accept, regexp='^Принять дуэль$')
    dp.register_message_handler(attack, state=Fight.Ready ,regexp='^Ебашь$')

