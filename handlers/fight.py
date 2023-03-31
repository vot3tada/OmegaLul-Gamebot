from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from utils.create_bot import dp, bot
import os
import random
import Classes.Player as Player

fights : dict[int, list[int, int]] = {}

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

def fightsFind(chat_id:int, player_id : int):
    for i in range(len(fights[chat_id])):
        if fights[chat_id][i][0] == player_id or fights[chat_id][i][1] == player_id:
            return i
    return -1

async def InitAttackStep(message: types.CallbackQuery):
    index = fightsFind(message.message.chat.id, message.from_user.id) 
    st1 : FSMContext = dp.current_state(chat=message.message.chat.id, user=fights[message.message.chat.id][index][0])
    st2 : FSMContext = dp.current_state(chat=message.message.chat.id, user=fights[message.message.chat.id][index][1])
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
        name1 = Player.GetPlayer(f'{message.message.chat.id}_{message.message.from_user.id}').name
        name2 = Player.GetPlayer(f'{message.message.chat.id}_{message.message.from_user.id}').name
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
            keyboard.add(types.InlineKeyboardButton(text="Драться яростно", callback_data=f"fightR:{fights[message.message.chat.id][index][0]}_{fights[message.message.chat.id][index][1]}"))
            keyboard.add(types.InlineKeyboardButton(text="Драться ловко", callback_data=f"fightD:{fights[message.message.chat.id][index][0]}_{fights[message.message.chat.id][index][1]}"))

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
            fights[message.message.chat.id].pop(index)
            await message.message.answer_photo(photo, caption=replyText)

async def fight_call(message : types.Message):
    if not message.chat.id in fights.keys():
        fights[message.chat.id] = []

    if not Player.FindPlayer(f'{message.chat.id}_{message.from_user.id}'):
        await message.reply('Ты не зареган, боец')
        return
    playerTo = Player.GetPlayer(f'{message.chat.id}_{message.from_user.id}')
    if not message.reply_to_message is None:
        if message.reply_to_message.from_user.id == (await bot.get_me()).id:
            await message.answer('Омегалюль вам не по зубам, салага')
            return
        if not Player.GetPlayer(f'{message.chat.id}_{message.reply_to_message.from_user.id}'):
            await message.reply('Этот боец не зареган')
            return
        playerFrom = Player.GetPlayer(f'{message.chat.id}_{message.reply_to_message.from_user.id}')
        index = fightsFind(message.chat.id, message.from_user.id) 
        if index != -1:
            if fights[message.chat.id][index][0] == message.from_user.id:
                await message.reply('Незя кинуть сразу две перчатки, отмените прошлую дуэль')
            else:
                await message.reply('Этому войну уже кинули перчатку')
            return
        if message.reply_to_message.from_user.id == message.from_user.id:
            await message.reply('Незя дуэлиться с шизой')
            return
        fights[message.chat.id].append([message.from_user.id, message.reply_to_message.from_user.id])
        await message.answer(f'{playerTo.name} бросил вызов {playerFrom.name}!')
    else:
        await message.answer(f'С кем дуэль то, {playerTo.name} ?')

async def fight_refuse(message: types.Message, state :FSMContext):
    if not message.chat.id in fights.keys():
        fights[message.chat.id] = []
    index = fightsFind(message.chat.id, message.from_user.id)
    if index == -1:
        await message.answer("Нечего отменять")
    else:
        if await state.get_state() == 'Fight:Ready' or await state.get_state() == 'Fight:Attack':
            st = dp.current_state(chat= message.chat.id, user=fights[message.chat.id][index][0])
            st.finish()
            st = dp.current_state(chat= message.chat.id, user=fights[message.chat.id][index][1])
            st.finish()
            reply_text = f'{message.from_user.full_name} позорно бежит с поля боя!\n'
        else:
            reply_text = f'{message.from_user.full_name} отказался от дуэли!\n'
        fights[message.chat.id].pop(index)
        await message.answer(reply_text)

async def fight_accept(message: types.Message):
    if not message.chat.id in fights.keys():
        fights[message.chat.id] = []
    index = fightsFind(message.chat.id, message.from_user.id)
    if index == -1 or fights[message.chat.id][index][0] == message.from_user.id:
        await message.answer("Нечего принимать")
    else:
        st : FSMContext = dp.current_state(chat=message.chat.id, user=fights[message.chat.id][index][0])
        await st.set_state(Fight.Ready)
        user1 = Player.GetPlayer(f'{message.chat.id}_{fights[message.chat.id][index][0]}')
        fighterData = fighter.copy()
        fighterData['health'] = user1.hp
        fighterData['damage'] = user1.damage * user1.damageMultiply
        fighterData['luck'] = user1.luck * user1.luckMultiply
        await st.set_data(fighterData)
        st : FSMContext = dp.current_state(chat=message.chat.id, user=fights[message.chat.id][index][1])
        await st.set_state(Fight.Ready)
        user2 = Player.GetPlayer(f'{message.chat.id}_{fights[message.chat.id][index][1]}')
        fighterData = fighter.copy()
        fighterData['health'] = user2.hp
        fighterData['damage'] = user2.damage * user2.damageMultiply
        fighterData['luck'] = user2.luck * user2.luckMultiply
        await st.set_data(fighter)

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Драться яростно", callback_data=f"fightR:{fights[message.chat.id][index][0]}_{fights[message.chat.id][index][1]}"))
        keyboard.add(types.InlineKeyboardButton(text="Драться ловко", callback_data=f"fightD:{fights[message.chat.id][index][0]}_{fights[message.chat.id][index][1]}"))

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
    dp.register_message_handler(fight_refuse, state=[None,Fight.Ready,Fight.Attack], regexp='^Отменить дуэль$')
    dp.register_message_handler(fight_accept, state=None ,regexp='^Принять дуэль$')
    dp.register_callback_query_handler(RageAttack, state=Fight.Ready, regexp='^fightR:*')
    dp.register_callback_query_handler(DexAttack, state=Fight.Ready, regexp='^fightD:*')


