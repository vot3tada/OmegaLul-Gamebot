from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from utils.create_bot import dp, bot
import os
import random
import Classes.Player as Player
from utils.scheduler import scheduler

def ExpReward(hp: int) -> int:
    return 50 + 100 * (100 - hp)//(100)

def MoneyReward(hp: int) -> int:
    return 10 + 25 * (100 - hp)//(100)

HPCut : int = 10
UltaCharge: int = 4

fights : dict[int, list[int, int]] = {}

class Fight(StatesGroup):
    Ready = State()
    Attack = State()

fighter = {
    'health':100,
    'luck':0.2,
    'damage':25,
    'rageFactor':0,
    'dexFactor': 0,
    'defence': 1,
    'ulta': 0,
    'charge': 0
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

        scheduler.reschedule_job(f'fight_{message.message.chat.id}_{fights[message.message.chat.id][index][0]}_{fights[message.message.chat.id][index][1]}', 
                                 trigger='interval', minutes=1.5)

        st1d = await st1.get_data()
        st2d = await st2.get_data()
        #Рассчет уворота
        lk1 = 1 if random.random() // (st1d.get('luck') + (st1d.get('luck') * 0.55 * st1d.get('dexFactor')) ) > 0 else 0
        lk2 = 1 if random.random() // (st2d.get('luck') + (st2d.get('luck') * 0.55 * st2d.get('dexFactor')) ) > 0 else 0
        #Рассчет урона
        dmg2 = (st1d.get('defence') * st2d.get('defence') * (st2d.get('damage') + 
                            (st2d.get('damage') * 0.15 * st2d.get('rageFactor')) +
                            (st2d.get('damage') * st2d.get('ulta')))
                            )
        dmg1 = (st2d.get('defence') * st1d.get('defence') * (st1d.get('damage') + 
                            (st1d.get('damage') * 0.15 * st1d.get('rageFactor')) +
                            (st1d.get('damage') * st1d.get('ulta')))
                            )
        await st1.update_data(
            health = ( st1d.get('health') - lk1 * dmg2))
        await st2.update_data(
            health = ( st2d.get('health') - lk2 * dmg1))
        replyText = random.choice(fight_texts) 
        player1 = Player.GetPlayer(message.message.chat.id, fights[message.message.chat.id][index][0])
        name1 = player1.name
        player2 = Player.GetPlayer(message.message.chat.id, fights[message.message.chat.id][index][1])
        name2 = player2.name
        
        if st1d.get('ulta'):
            replyText += f'{name1} ультует и'
        elif not st1d.get('defence'):
            replyText += f'{name1} защищается и'
        elif lk1 == 0: 
            replyText += f'{name1} уворачивается и'
        else:
            replyText += f'{name1}'
        replyText += f' наносит {dmg1} урона!\n'

        if st2d.get('ulta'):
            replyText += f'{name2} ультует и'
        elif not st2d.get('defence'):
            replyText += f'{name2} защищается и'
        elif lk2 == 0: 
            replyText += f'{name2} уворачивается и'
        else:
            replyText += f'{name2}'
        replyText += f' наносит {dmg2} урона!\n'

        await st1.update_data(charge = st1d.get('charge') + 1)
        await st2.update_data(charge = st2d.get('charge') + 1)

        st1d = await st1.get_data()
        st2d = await st2.get_data()
        
        replyText += f'<b>Здоровье бойцов</b>:\n{name1}: {st1d.get("health")}\n{name2}: {st2d.get("health")}\n'
        replyText += f'<b>Заряд бойцов</b>:\n{name1}: {st1d.get("charge")}\\{UltaCharge}\n{name2}: {st2d.get("charge")}\\{UltaCharge}\n'

        photo = open(f'./static/fight/{random.choice(fight_images)}',"rb")
        if st1d.get("health") > 0 and st2d.get("health") > 0:
            await st1.set_state(Fight.Ready)
            await st2.set_state(Fight.Ready)

            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Драться яростно", callback_data=f"fightR:{fights[message.message.chat.id][index][0]}_{fights[message.message.chat.id][index][1]}"))
            keyboard.add(types.InlineKeyboardButton(text="Драться ловко", callback_data=f"fightD:{fights[message.message.chat.id][index][0]}_{fights[message.message.chat.id][index][1]}"))
            keyboard.add(types.InlineKeyboardButton(text="УЛЬТАНУТЬ", callback_data=f"ulta:{fights[message.message.chat.id][index][0]}_{fights[message.message.chat.id][index][1]}"))
            keyboard.add(types.InlineKeyboardButton(text="Защищаться", callback_data=f"defence:{fights[message.message.chat.id][index][0]}_{fights[message.message.chat.id][index][1]}"))
            
            await message.message.answer_photo(photo, caption=replyText, reply_markup=keyboard, parse_mode='HTML')
        else:
            scheduler.remove_job(f'fight_{message.message.chat.id}_{fights[message.message.chat.id][index][0]}_{fights[message.message.chat.id][index][1]}')
            await st1.finish()
            await st2.finish()
            if st1d.get("health") > 0 and  st2d.get("health") <= 0:
                replyText += f'Победитель: {name1}!!\nХвала чемпиону зверей!\n'
                exp = ExpReward(player1.hp)
                money = MoneyReward(player1.hp)
                player1.exp += exp
                player1.money += money
                replyText += f'<b>Получено</b>:\nОпыт: {exp}\nДеньги: {money}'
            elif st2d.get("health") > 0 and  st1d.get("health") <= 0:
                replyText += f'Победитель: {name2}!!\nХвала чемпиону зверей!\n'
                exp = ExpReward(player2.hp)
                money = MoneyReward(player2.hp)
                player2.exp += exp
                player2.money += money
                replyText += f'<b>Получено</b>:\nОпыт: {exp}\nДеньги: {money}'
            else:
                replyText += f'Победителя нет! Оба бойца ушатали друг друга!\nНикогда такого не было и вот опять...'
            player1.hp -= HPCut
            player2.hp -= HPCut
            fights[message.message.chat.id].pop(index)
            await message.message.answer_photo(photo, caption=replyText, parse_mode='HTML')

async def fight_call(message : types.Message):
    if not message.chat.id in fights.keys():
        fights[message.chat.id] = []

    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Ты не зареган, боец')
        return
    playerTo = Player.GetPlayer(message.chat.id, message.from_user.id)

    if not playerTo.hp:
        await message.reply('Твое здоровье на нуле, боец')
        return

    if not message.reply_to_message is None:
        if message.reply_to_message.from_user.id == (await bot.get_me()).id:
            await message.answer('Омегалюль вам не по зубам, салага')
            return
        if not Player.FindPlayer(message.chat.id, message.reply_to_message.from_user.id):
            await message.reply('Этот боец не зареган')
            return
        playerFrom = Player.GetPlayer(message.chat.id, message.reply_to_message.from_user.id)
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
        index = fightsFind(message.chat.id, message.from_user.id) 
        scheduler.add_job(OutOfTimeFight,'interval', minutes=1.5, args=[message.chat.id, index], jobstore='local' ,id=f'fight_{message.chat.id}_{fights[message.chat.id][index][0]}_{fights[message.chat.id][index][1]}')
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
        user1 = Player.GetPlayer(message.chat.id, message.from_user.id)
        if await state.get_state() == 'Fight:Ready' or await state.get_state() == 'Fight:Attack':
            st = dp.current_state(chat= message.chat.id, user=fights[message.chat.id][index][0])
            await st.finish()
            st = dp.current_state(chat= message.chat.id, user=fights[message.chat.id][index][1])
            user2 = Player.GetPlayer(message.chat.id, fights[message.chat.id][index][1])
            await st.finish()
            
            user1.hp -= HPCut
            user2.hp -= HPCut
            exp = ExpReward(user2.hp)
            money = MoneyReward(user2.hp)
            user2.exp += exp
            user2.money += money

            reply_text = f'{user1.name} позорно бежит с поля боя!\n{user2.name} победил!\n<b>Получено:</b>\nОпыт: {exp}\nДеньги: {money}'
            scheduler.remove_job(f'fight_{message.chat.id}_{fights[message.chat.id][index][0]}_{fights[message.chat.id][index][1]}')
        else:
            reply_text = f'{user1.name} отказался от дуэли!\n'
        fights[message.chat.id].pop(index)
        await message.answer(reply_text, parse_mode='HTML')

async def fight_accept(message: types.Message):
    if not message.chat.id in fights.keys():
        fights[message.chat.id] = []
    index = fightsFind(message.chat.id, message.from_user.id)
    if index == -1 or fights[message.chat.id][index][0] == message.from_user.id:
        await message.answer("Нечего принимать")
    else:
        st : FSMContext = dp.current_state(chat=message.chat.id, user=fights[message.chat.id][index][0])
        await st.set_state(Fight.Ready)
        user1 = Player.GetPlayer(message.chat.id, fights[message.chat.id][index][0])
        fighterData = fighter.copy()
        fighterData['health'] = user1.hp
        fighterData['damage'] = user1.damage * user1.damageMultiply
        fighterData['luck'] = user1.luck * user1.luckMultiply
        await st.set_data(fighterData)
        st : FSMContext = dp.current_state(chat=message.chat.id, user=fights[message.chat.id][index][1])
        await st.set_state(Fight.Ready)
        user2 = Player.GetPlayer(message.chat.id, fights[message.chat.id][index][1])
        fighterData = fighter.copy()
        fighterData['health'] = user2.hp
        fighterData['damage'] = user2.damage * user2.damageMultiply
        fighterData['luck'] = user2.luck * user2.luckMultiply
        await st.set_data(fighterData)

        scheduler.reschedule_job(f'fight_{message.chat.id}_{fights[message.chat.id][index][0]}_{fights[message.chat.id][index][1]}', 
                                 trigger='interval', minutes=1.5)

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Драться яростно", callback_data=f"fightR:{fights[message.chat.id][index][0]}_{fights[message.chat.id][index][1]}"))
        keyboard.add(types.InlineKeyboardButton(text="Драться ловко", callback_data=f"fightD:{fights[message.chat.id][index][0]}_{fights[message.chat.id][index][1]}"))
        keyboard.add(types.InlineKeyboardButton(text="УЛЬТАНУТЬ", callback_data=f"ulta:{fights[message.chat.id][index][0]}_{fights[message.chat.id][index][1]}"))
        keyboard.add(types.InlineKeyboardButton(text="Защищаться", callback_data=f"defence:{fights[message.chat.id][index][0]}_{fights[message.chat.id][index][1]}"))

        media = types.MediaGroup()
        media.attach_photo(types.InputFile(user1.photo), 'Битва этих двух ронинов начинается!!!')
        media.attach_photo(types.InputFile(user2.photo))

        await message.answer_media_group(media)
        await message.answer("<b>!!FIGHT!!</b>",reply_markup=keyboard, parse_mode='HTML')

async def RageAttack(call: types.CallbackQuery, state : FSMContext):

    user1, user2 = call.data.replace("fightR:",'').split('_')

    if str(call.from_user.id) != user1 and str(call.from_user.id) != user2:
        await call.answer("Это не ваша битва...")
        return
    
    index = fightsFind(call.message.chat.id, call.from_user.id)
    if index == -1:
        await call.answer("Это битва уже только в воспоминаниях...")
        return
    
    await state.set_state(Fight.Attack)
    await state.update_data(rageFactor = 1, dexFactor = 0, defence = 1, ulta = 0)
    await InitAttackStep(call)
    await call.answer('Вы сделали свой выбор')

async def DexAttack(call: types.CallbackQuery, state : FSMContext):

    user1, user2 = call.data.replace("fightD:",'').split('_')

    if str(call.from_user.id) != user1 and str(call.from_user.id) != user2:
        await call.answer("Это не ваша битва...")
        return
    
    index = fightsFind(call.message.chat.id, call.from_user.id)
    if index == -1:
        await call.answer("Это битва уже только в воспоминаниях...")
        return

    await state.set_state(Fight.Attack)
    await state.update_data(rageFactor = 0, dexFactor = 1, defence = 1, ulta = 0)
    await InitAttackStep(call)
    await call.answer('Вы сделали свой выбор')

async def Ulta(call: types.CallbackQuery, state: FSMContext):

    user1, user2 = call.data.replace("ulta:",'').split('_')

    if str(call.from_user.id) != user1 and str(call.from_user.id) != user2:
        await call.answer("Это не ваша битва...")
        return
    
    index = fightsFind(call.message.chat.id, call.from_user.id)
    if index == -1:
        await call.answer("Это битва уже только в воспоминаниях...")
        return
    
    std = await state.get_data()
    if std.get('charge') < UltaCharge:
        await call.answer('Ультовать еще нельзя')
        return
    
    await state.update_data(charge = 0)
    await state.set_state(Fight.Attack)
    await state.update_data(rageFactor = 0, dexFactor = 0, defence = 1, ulta = 1)
    await InitAttackStep(call)
    await call.answer('Вы сделали свой выбор')

async def Defence(call: types.CallbackQuery, state: FSMContext):

    user1, user2 = call.data.replace("defence:",'').split('_')

    if str(call.from_user.id) != user1 and str(call.from_user.id) != user2:
        await call.answer("Это не ваша битва...")
        return
    
    index = fightsFind(call.message.chat.id, call.from_user.id)
    if index == -1:
        await call.answer("Это битва уже только в воспоминаниях...")
        return

    await state.set_state(Fight.Attack)
    await state.update_data(rageFactor = 0, dexFactor = 0, defence = 0, ulta = 0)
    await InitAttackStep(call)
    await call.answer('Вы сделали свой выбор')


async def OutOfTimeFight(chatId: int, fightIndex: int):

    scheduler.remove_job(f'fight_{chatId}_{fights[chatId][fightIndex][0]}_{fights[chatId][fightIndex][1]}')

    st1 : FSMContext = dp.current_state(chat=chatId, user=fights[chatId][fightIndex][0])
    st2 : FSMContext = dp.current_state(chat=chatId, user=fights[chatId][fightIndex][1])
    st1s = await st1.get_state()
    st2s = await st2.get_state()

    player1: Player.Player = Player.GetPlayer(chatId, fights[chatId][fightIndex][0])
    player2: Player.Player = Player.GetPlayer(chatId, fights[chatId][fightIndex][1])

    fights[chatId].pop(fightIndex)

    if not st2s in ['Fight:Ready', 'Fight:Attack']:
        await bot.send_message(chat_id=chatId, text=f'{player2.name} не принял дуэль от {player1.name}\n')
        return
    
    await st1.set_state(None)
    await st2.set_state(None)
    
    player1.hp -= 10
    player2.hp -= 10
    if st1s == 'Fight:Ready' and st2s == 'Fight:Ready':
        await bot.send_message(
                        chat_id=chatId,
                        text='Оба бойца тихо разошлись...но осадочек остался')
    elif st1s == 'Fight:Ready':
        exp = ExpReward(player2.hp)
        money = MoneyReward(player2.hp)
        player2.exp += exp
        player2.money += money
        await bot.send_message(
                        chat_id=chatId,
                        parse_mode="HTML",
                        text=f'{player1.name} думал, думал... и в суп попал!\n{player2.name} победил!\n<b>Получено:</b>\nОпыт: {exp}\nДеньги: {money}')
    else:
        exp = ExpReward(player1.hp)
        money = MoneyReward(player1.hp)
        player1.exp += exp
        player1.money += money
        await bot.send_message(
                        chat_id=chatId,
                        parse_mode="HTML",
                        text=f'{player2.name} думал, думал... и в суп попал!\n{player1.name} победил!\n<b>Получено:</b>\nОпыт: {exp}\nДеньги: {money}')

#################################################
def register_fight_handlers(dp : Dispatcher):
    dp.register_message_handler(fight_call, state=None, commands='duel')
    dp.register_message_handler(fight_refuse, state=[None,Fight.Ready,Fight.Attack], commands='duel_refuse')
    dp.register_message_handler(fight_accept, state=None ,commands='duel_accept')
    dp.register_callback_query_handler(RageAttack, state=Fight.Ready, regexp='^fightR:*')
    dp.register_callback_query_handler(DexAttack, state=Fight.Ready, regexp='^fightD:*')
    dp.register_callback_query_handler(Defence, state=Fight.Ready, regexp='^defence:*')
    dp.register_callback_query_handler(Ulta, state=Fight.Ready, regexp='^ulta:*')


