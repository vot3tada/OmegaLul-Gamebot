from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
import os
import random

fights = []

class Fight(StatesGroup):
    Ready = State()
    Attack = State()

fighter = {
    'health':100,
    'luck':0.2,
    'damage':25,
    'rageFactor':0,
    'dexFactor': 0
}

fight_images = os.listdir('./static/fight')
fight_texts = [
    'Каждую пятницу одно и тоже!\n',
    'Заходи! Сбоку заходи!\n',
    'Кранты вам всем!!\n',
    'Ааа, ща мы вам, арабы недоделанные!\n',
    'Выноси бычьё!\n'
]

def fightsFind(id : int):
    for i in range(len(fights)):
        if fights[i][0] == id or fights[i][1] == id:
            return i
    return -1

async def InitAttackStep(message: types.CallbackQuery):
    index = fightsFind(message.from_user.id) 
    st1 : FSMContext = dp.current_state(chat=message.message.chat.id, user=fights[index][0])
    st2 : FSMContext = dp.current_state(chat=message.message.chat.id, user=fights[index][1])
    st1s = await st1.get_state()
    st2s = await st2.get_state()
    if st1s == 'Fight:Attack' and st2s == 'Fight:Attack':
        st1d = await st1.get_data()
        st2d = await st2.get_data()
        lk1 = 1 if random.random() // (st1d.get('luck') + (st1d.get('luck') * 0.5 * st1d.get('dexFactor')) ) > 0 else 0
        lk2 = 1 if random.random() // (st2d.get('luck') + (st2d.get('luck') * 0.5 * st2d.get('dexFactor')) ) > 0 else 0

        await st1.update_data(
            health = ( st1d.get('health') - 
                      (lk1 * (st2d.get('damage') + 
                              (st2d.get('damage') * 0.2 * st2d.get('rageFactor')))))
        )
        await st2.update_data(
            health = ( st2d.get('health') - 
                      (lk2 * (st1d.get('damage') + 
                              (st1d.get('damage') * 0.2 * st1d.get('rageFactor')))))
        )
        replyText = random.choice(fight_texts) 
        name1 = (await bot.get_chat_member(chat_id=message.message.chat.id, user_id=fights[index][0])).user.full_name
        name2 = (await bot.get_chat_member(chat_id=message.message.chat.id, user_id=fights[index][1])).user.full_name
        if lk1 == 0: 
            replyText += f'{name1} словил(а) удачу и уворачивается от урона!\n'
        else:
            replyText += f'{name1} упустил(а) удачу и получил(а) по самые помидоры!\n'
        if lk2 == 0: 
            replyText += f'{name2} словил(а) удачу и уворачивается от урона!\n'
        else:
            replyText += f'{name2} упустил(а) удачу и получил(а) по самые помидоры!\n'
        st1d = await st1.get_data()
        st2d = await st2.get_data()
        
        replyText += f'Здоровье бойцов:\n{name1}: {st1d.get("health")}\n{name2}: {st2d.get("health")}\n'

        photo = open(f'./static/fight/{random.choice(fight_images)}',"rb")
        if st1d.get("health") > 0 and st2d.get("health") > 0:
            await st1.set_state(Fight.Ready)
            await st2.set_state(Fight.Ready)

            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Драться яростно", callback_data=f"fightR:{fights[index][0]}_{fights[index][1]}"))
            keyboard.add(types.InlineKeyboardButton(text="Драться ловко", callback_data=f"fightD:{fights[index][0]}_{fights[index][1]}"))

            await message.message.answer_photo(photo, caption=replyText, reply_markup=keyboard)
        else:
            await st1.finish()
            await st2.finish()
            if st1d.get("health") > 0 and  st2d.get("health") <= 0:
                replyText += f'Победитель: {name1}!!\nХвала чемпиону зверей!'
            elif st2d.get("health") > 0 and  st1d.get("health") <= 0:
                replyText += f'Победитель: {name2}!!\nХвала чемпиону зверей!'
            else:
                replyText += f'Победителя нет! Оба бойца ушатали друг друга!\nНикогда такого не было и вот опять...'
            fights.pop(index)
            await message.message.answer_photo(photo, caption=replyText)

async def fight_call(message : types.Message):
    from .registration import users
    if str(message.from_user.id) not in users.keys():
        await message.reply('Ты не зареган, боец')
        return
    if message.reply_to_message is not None:
        if (str(message.reply_to_message.from_user.id)) not in users.keys():
            await message.reply('Этот боец не зареган')
            return
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
        await message.answer(f'{message.from_user.full_name} бросил вызов {message.reply_to_message.from_user.full_name}!')
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
    from .registration import users
    index = fightsFind(message.from_user.id)
    if index == -1 or fights[index][0] == message.from_user.id:
        await message.answer("Нечего принимать")
    else:
        st : FSMContext = dp.current_state(chat=message.chat.id, user=fights[index][0])
        await st.set_state(Fight.Ready)
        user = users[str(fights[index][0])]
        fighterData = fighter.copy()
        fighterData['health'] = user.hp
        fighterData['damage'] = user.damage * user.damageMultiply
        fighterData['luck'] = user.luck * user.luckMultiply
        await st.set_data(fighterData)
        st : FSMContext = dp.current_state(chat=message.chat.id, user=fights[index][1])
        await st.set_state(Fight.Ready)
        user = users[str(fights[index][1])]
        fighterData = fighter.copy()
        fighterData['health'] = user.hp
        fighterData['damage'] = user.damage * user.damageMultiply
        fighterData['luck'] = user.luck * user.luckMultiply
        await st.set_data(fighter)
        fights[index][2] = True

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Драться яростно", callback_data=f"fightR:{fights[index][0]}_{fights[index][1]}"))
        keyboard.add(types.InlineKeyboardButton(text="Драться ловко", callback_data=f"fightD:{fights[index][0]}_{fights[index][1]}"))

        user1 = users[str(fights[index][0])]
        user2 = users[str(fights[index][1])]
        media = types.MediaGroup()
        media.attach_photo(types.InputFile(user1.photo), 'Битва этих двух ронинов начинается!!!')
        media.attach_photo(types.InputFile(user2.photo))

        await message.answer_media_group(media)
        await message.answer("!!FIGHT!!",reply_markup=keyboard)

async def RageAttack(call: types.CallbackQuery, state : FSMContext):

    user1, user2 = call.data.replace("fightR:",'').replace("fightD:",'').split('_')

    if str(call.from_user.id) != user1 and str(call.from_user.id) != user2:
        await call.answer("Это не ваша битва...")
        return
    
    await state.set_state(Fight.Attack)
    await state.update_data(rageFactor = 1, dexFactor = 0)
    await InitAttackStep(call)
    await call.answer()

async def DexAttack(call: types.CallbackQuery, state : FSMContext):

    user1, user2 = call.data.replace("fightR:",'').replace("fightD:",'').split('_')

    if str(call.from_user.id) != user1 and str(call.from_user.id) != user2:
        await call.answer("Это не ваша битва...")
        return
    
    await state.set_state(Fight.Attack)
    await state.update_data(rageFactor = 0, dexFactor = 1)
    await InitAttackStep(call)
    await call.answer()


#################################################
def register_fight_handlers(dp : Dispatcher):
    dp.register_message_handler(fight_call, state=None, regexp='^Дуэль$')
    dp.register_message_handler(fight_refuse, state=[None,Fight.Ready], regexp='^Отменить дуэль$')
    dp.register_message_handler(fight_accept, state=None ,regexp='^Принять дуэль$')
    dp.register_callback_query_handler(RageAttack, state=Fight.Ready, regexp='^fightR:*')
    dp.register_callback_query_handler(DexAttack, state=Fight.Ready, regexp='^fightD:*')


