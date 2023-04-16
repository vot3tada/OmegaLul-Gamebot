from typing import Any
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import Classes.Player as Player
from utils.scheduler import scheduler
from utils.create_bot import dp, bot
from Classes.Fighter import *
import random
import os

collectorFight: list[Player.Player] = []

collectorFighter = {
    'cHealth':130,
    'cLuck':0.2,
    'cDamage':25,
    'cRageFactor':0,
    'cDexFactor': 0,
    'cDefence': 1,
    'cUlta': 0,
    'cCharge': 0,
    'cMoney': 0
}

def fightsFind(chatId: int, userId: int):
    for player in collectorFight:
        if player.userId == userId and player.chatId == chatId:
            return True
    return False

def fightsDelete(chatId: int, userId: int):
    for player in collectorFight:
        if player.userId == userId and player.chatId == chatId:
            collectorFight.remove(player)
            return
        
def GetCollectorChoice(fighterData: dict[str, Any]) -> dict[str, Any]:
    if fighterData['charge'] == UltaCharge:
        return {
            'cRageFactor':0,
            'cDexFactor': 0,
            'cDefence': 0,
            'cUlta': 0,
        }
    if fighterData['cCharge'] - 1 == UltaCharge:
        if random.random() * 0.1 + fighterData['cCharge'] > 0.65:
            return {
            'cRageFactor':0,
            'cDexFactor': 0,
            'cDefence': 1,
            'cUlta': 1,
            'cCharge': 0
        }
    if random.random() > 0.6:
        if random.random() * 0.1 + fighterData['cCharge'] > 0.65:
            return {
            'cRageFactor':1,
            'cDexFactor': 0,
            'cDefence': 1,
            'cUlta': 0,
        }
    else:
        return {
            'cRageFactor':0,
            'cDexFactor': 1,
            'cDefence': 1,
            'cUlta': 0,
        }

async def InitAttackStep(call: types.CallbackQuery):
    scheduler.reschedule_job(f'collectorFight_{call.message.chat.id}_{call.from_user.id}', 
                                 trigger='interval', minutes=1.5)
    
    st : FSMContext = dp.current_state(chat=call.message.chat.id, user=call.from_user.id)
    std = await st.get_data()
    lk1 = 1 if random.random() // (std.get('luck') + (std.get('luck') * 0.55 * std.get('dexFactor')) ) > 0 else 0
    lk2 = 1 if random.random() // (std.get('cLuck') + (std.get('cLuck') * 0.55 * std.get('cDexFactor')) ) > 0 else 0

    dmg2 =  (std.get('defence') * std.get('cDefence') * (std.get('cDamage') + 
                        (std.get('cDamage') * 0.15 * std.get('cRageFactor')) +
                        (std.get('cDamage') * std.get('cUlta'))) )
    dmg1 =  (std.get('cDefence') * std.get('defence') * (std.get('damage') + 
                        (std.get('damage') * 0.15 * std.get('rageFactor')) +
                        (std.get('damage') * std.get('ulta'))) )
    await st.update_data(
        health = ( std.get('health') - lk1 * dmg2),
        cHealth = ( std.get('cHealth') - lk2 * dmg1)
    )
    replyText = random.choice(fight_texts) 
    player = Player.GetPlayer(call.message.chat.id, call.from_user.id)

    if std.get('ulta') and lk1 == 0:
        replyText += f'{player.name} ультует, уворачивается и'
    elif std.get('ulta'):
        replyText += f'{player.name} ультует и'
    elif not std.get('defence'):
        replyText += f'{player.name} защищается и'
    elif lk1 == 0: 
        replyText += f'{player.name} уворачивается и'
    else:
        replyText += f'{player.name}'
    replyText += f' наносит {dmg1} урона!\n'

    if std.get('cUlta') and lk2 == 0:
        replyText += f'Коллектор ультует, уворачивается и'
    elif std.get('cUlta'):
        replyText += f'Коллектор ультует и'
    elif not std.get('cDefence'):
        replyText += f'Коллектор защищается и'
    elif lk2 == 0: 
        replyText += f'Коллектор уворачивается и'
    else:
        replyText += f'Коллектор'
    replyText += f' наносит {dmg2} урона!\n'

    await st.update_data(
        charge = std.get('charge') + 1,
        cCharge = std.get('cCharge') + 1
    )

    std = await st.get_data()

    replyText += f'<b>Здоровье бойцов</b>:\n{player.name}: {std.get("health")}\nКоллектор: {std.get("cHealth")}\n'
    replyText += f'<b>Заряд бойцов</b>:\n{player.name}: {std.get("charge")}\\{UltaCharge}\nКоллектор: {std.get("cCharge")}\\{UltaCharge}\n'
    media: types.InputMedia = None
    if std.get("health") > 0 and std.get("cHealth") > 0:
        
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Драться яростно", callback_data=f"collectorFightR:{player.chatId}_{player.userId}"))
        keyboard.add(types.InlineKeyboardButton(text="Драться ловко", callback_data=f"collectorFightD:{player.chatId}_{player.userId}"))
        keyboard.add(types.InlineKeyboardButton(text="УЛЬТАНУТЬ", callback_data=f"collectorUlta:{player.chatId}_{player.userId}"))
        keyboard.add(types.InlineKeyboardButton(text="Защищаться", callback_data=f"collectorDefence:{player.chatId}_{player.userId}"))

        media = types.input_media.InputMediaPhoto(media=types.InputFile('./static/fight/' + random.choice(os.listdir('./static/fight'))), caption=replyText, parse_mode='HTML')
        await call.message.edit_media(media, reply_markup=keyboard)
        await st.set_state(CollectorState.Ready)
    else:
        scheduler.remove_job(f'collectorFight_{call.message.chat.id}_{call.from_user.id}')
        await st.finish()
        if std.get("health") > 0 and  std.get("cHealth") <= 0:
            replyText += f'Победитель: {player.name}!!\nХвала чемпиону коллекторов!\n'
            exp = ExpReward(player.hp)
            money = MoneyReward(player.hp)
            player.exp += exp
            player.money += money
            replyText += f'<b>Получено</b>:\nОпыт: {exp}\nДеньги: {money}'
            media = types.input_media.InputMediaPhoto(media=types.InputFile('./static/win/' + random.choice(os.listdir('./static/win'))), caption=replyText, parse_mode='HTML')
        elif std.get("cHealth") > 0 and  std.get("health") <= 0:
            replyText += f'Победитель: Коллектор!!\nЕще один должник получил по заслугам!\n'
            money = int(std.get('cMoney'))
            if player.money < money:
                player.money = 0
            else:
                player.money -= money
            replyText += f'Коллектор забрал {money} денег, еще и покалечил...'
            media = types.input_media.InputMediaPhoto(media=types.InputFile('./static/lose/' + random.choice(os.listdir('./static/lose'))), caption=replyText, parse_mode='HTML')
        else:      
            replyText += f'Победителя нет! Оба бойца ушатали друг друга!\nНикогда такого не было и вот опять...'
            media = types.input_media.InputMediaPhoto(media=types.InputFile('./static/lose/' + random.choice(os.listdir('./static/lose'))), caption=replyText, parse_mode='HTML')
        player.hp -= HPCut
        fightsDelete(player.chatId, player.userId)

        await call.message.edit_media(media=media)

class CollectorState(StatesGroup):
    Punished = State()
    Ready = State()
    Attack = State()

async def payCollector(call: types.CallbackQuery, state: FSMContext):
    chatId, userId, money = call.data.replace("collectorPay:",'').split('_')
    try:
        chatId = int(chatId)
        userId = int(userId)
        money = float(money)
    except:
        await call.answer()
        return
    player: Player.Player = Player.GetPlayer(chatId, userId)
    if player.money < money:
        player.money = 0
        await call.message.answer(f"{player.name} отдает коллектору что было и уйти с миром...")
        await state.finish()
        return
    else:
        player.money -= money
        await call.message.answer(f"{player.name} отдает коллектору налог на разгильдяйство.")
        await state.finish()
        return

async def fightCollector(call: types.CallbackQuery, state: FSMContext):
    chatId, userId, money = call.data.replace("collectorFight:",'').split('_')
    try:
        chatId = int(chatId)
        userId = int(userId)
        money = float(money)
    except:
        await call.answer()
        return
    player: Player.Player = Player.GetPlayer(chatId, userId)
    if not player.hp:
        await call.answer('Твое здоровье на нуле, боец')
        return
    await call.message.answer(f"{player.name} остаивает свой сгоревший дедлайн, чтож...")
    await CollectorState.Ready.set()
    
    fighterData = dict(fighter, **collectorFighter)
    fighterData['health'] = player.hp
    fighterData['damage'] = player.damage * player.damageMultiply
    fighterData['luck'] = player.luck * player.luckMultiply
    fighterData['cMoney'] = money
    await state.set_data(fighterData)

    collectorFight.append(player)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Драться яростно", callback_data=f"collectorFightR:{player.chatId}_{player.userId}"))
    keyboard.add(types.InlineKeyboardButton(text="Драться ловко", callback_data=f"collectorFightD:{player.chatId}_{player.userId}"))
    keyboard.add(types.InlineKeyboardButton(text="УЛЬТАНУТЬ", callback_data=f"collectorUlta:{player.chatId}_{player.userId}"))
    keyboard.add(types.InlineKeyboardButton(text="Защищаться", callback_data=f"collectorDefence:{player.chatId}_{player.userId}"))
    scheduler.add_job(OutOfTimeFight,'interval', minutes=1.5, args=[player.chatId, player.userId, money], jobstore='local' ,id=f'collectorFight_{player.chatId}_{player.userId}')
    
    media = types.MediaGroup()
    media.attach_photo(types.InputFile(player.photo), 'Битва этих двух ронинов начинается!!!')
    media.attach_photo(types.InputFile('./static/collector/T801.jpg'))

    collectorHp = collectorFighter['cHealth']
    replyText = f'<b>Здоровье бойцов</b>:\n{player.name}: {player.hp}\nКоллектор: {collectorHp}\n'
    replyText += f'<b>Заряд бойцов</b>:\n{player.name}: {0}\\{UltaCharge}\nКоллектор: {0}\\{UltaCharge}\n'

    await call.message.answer_media_group(media)
    await call.message.answer_photo(photo=open('./static/fight/' + random.choice(os.listdir('./static/fight')), 'rb'),
                                    caption=replyText,
                                    reply_markup=keyboard, 
                                    parse_mode='HTML')

async def RageAttack(call: types.CallbackQuery, state : FSMContext):

    chatId, userId = call.data.replace("collectorFightR:",'').split('_')
    userId, chatId = int(userId), int(chatId)

    if call.from_user.id != userId or call.message.chat.id != chatId:
        await call.answer("Это не ваша битва...")
        return
    
    if not fightsFind(call.message.chat.id, call.from_user.id):
        await call.answer("Это битва уже только в воспоминаниях...")
        return
    
    await state.set_state(CollectorState.Attack)
    await state.update_data(GetCollectorChoice(await state.get_data()),rageFactor = 1, dexFactor = 0, defence = 1, ulta = 0)
    await InitAttackStep(call)
    await call.answer('Вы сделали свой выбор')

async def DexAttack(call: types.CallbackQuery, state : FSMContext):

    chatId, userId = call.data.replace("collectorFightD:",'').split('_')
    userId, chatId = int(userId), int(chatId)

    if call.from_user.id != userId or call.message.chat.id != chatId:
        await call.answer("Это не ваша битва...")
        return
    
    if not fightsFind(call.message.chat.id, call.from_user.id):
        await call.answer("Это битва уже только в воспоминаниях...")
        return
    
    await state.set_state(CollectorState.Attack)
    await state.update_data(GetCollectorChoice(await state.get_data()),rageFactor = 0, dexFactor = 1, defence = 1, ulta = 0)
    await InitAttackStep(call)
    await call.answer('Вы сделали свой выбор')

async def Ulta(call: types.CallbackQuery, state: FSMContext):

    chatId, userId = call.data.replace("collectorUlta:",'').split('_')
    userId, chatId = int(userId), int(chatId)

    if call.from_user.id != userId or call.message.chat.id != chatId:
        await call.answer("Это не ваша битва...")
        return
    
    if not fightsFind(call.message.chat.id, call.from_user.id):
        await call.answer("Это битва уже только в воспоминаниях...")
        return
    
    std = await state.get_data()
    if std.get('charge') < UltaCharge:
        await call.answer('Ультовать еще нельзя')
        return
    
    await state.update_data(charge = 0)
    await state.set_state(CollectorState.Attack)
    await state.update_data(GetCollectorChoice(await state.get_data()),rageFactor = 0, dexFactor = 0, defence = 1, ulta = 1)
    await InitAttackStep(call)
    await call.answer('Вы сделали свой выбор')

async def Defence(call: types.CallbackQuery, state: FSMContext):

    chatId, userId = call.data.replace("collectorDefence:",'').split('_')
    userId, chatId = int(userId), int(chatId)

    if call.from_user.id != userId or call.message.chat.id != chatId:
        await call.answer("Это не ваша битва...")
        return
    
    if not fightsFind(call.message.chat.id, call.from_user.id):
        await call.answer("Это битва уже только в воспоминаниях...")
        return
    
    await state.set_state(CollectorState.Attack)
    await state.update_data(GetCollectorChoice(await state.get_data()),rageFactor = 0, dexFactor = 0, defence = 0, ulta = 0)
    await InitAttackStep(call)
    await call.answer('Вы сделали свой выбор')

async def remindCollector(message: types.Message, state: FSMContext):

    await bot.send_message(
            chat_id=message.chat.id,
            reply_to_message_id=(await state.get_data()).get('messageId'),
            text=f'{message.from_user.mention} вас взял в заложники Коллектор')

async def OutOfTimeFight(chatId: int, userId: int, money: int):

    scheduler.remove_job(f'collectorFight_{chatId}_{userId}')

    st1 : FSMContext = dp.current_state(chat=chatId, user=userId)
    await st1.set_state(None)

    player: Player.Player = Player.GetPlayer(chatId, userId)

    fightsDelete(chatId, userId)
    
    player.hp -= 10
    if player.money < money:
        player.money = 0
    else:
        player.money -= money

    await bot.send_message(
        chat_id=chatId,
        parse_mode="HTML",
        text=f'{player.name} думал, думал... и в суп попал!\nКоллектор победил, отоборал {money} денег, еще и покалечил...')

def register_handlers_collector(dp: Dispatcher):
    dp.register_callback_query_handler(RageAttack, state=CollectorState.Ready, regexp='^collectorFightR:*')
    dp.register_callback_query_handler(DexAttack, state=CollectorState.Ready, regexp='^collectorFightD:*')
    dp.register_callback_query_handler(Defence, state=CollectorState.Ready, regexp='^collectorDefence:*')
    dp.register_callback_query_handler(Ulta, state=CollectorState.Ready, regexp='^collectorUlta:*')
    
    dp.register_callback_query_handler(payCollector, regexp='^collectorPay:*', state=CollectorState.Punished)
    dp.register_callback_query_handler(fightCollector, regexp='^collectorFight:*', state=CollectorState.Punished)
    dp.register_message_handler(remindCollector, state=CollectorState.Punished)