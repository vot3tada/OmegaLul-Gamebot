from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import Classes.Player as Player
import random
import os
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

IBMLuck = 0.37

async def startDiceGame(message: types.Message):
    text = 'Хе-хе, решили отобрать последние деньги у старого ЭйбиЭма ?\nНу, попробуйте...'
    keyboard=types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text='Начать игру в кости', callback_data=f'BetSet:')
    )
    await message.answer_photo(
        photo=open(ROOT / 'static/dice/' / random.choice(os.listdir(ROOT / 'static/dice')), 'rb'),
        caption=text,
        reply_markup=keyboard
    )

def GetBetKeyboard(bet: int, player: Player.Player) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    buttons: list[types.InlineKeyboardButton] = []
    if bet > 100:
        buttons.append(types.InlineKeyboardButton(text='<<', callback_data=f'BetReset:{player.userId}_{bet-100}'))
    else:
        buttons.append(types.InlineKeyboardButton(text='  ', callback_data=f'@$^'))

    if bet > 50:
        buttons.append(types.InlineKeyboardButton(text='<', callback_data=f'BetReset:{player.userId}_{bet-50}'))
    else:
        buttons.append(types.InlineKeyboardButton(text='  ', callback_data=f'@$^'))

    buttons.append(types.InlineKeyboardButton(text=bet, callback_data=f'@$^'))
    
    if player.money >= bet + 50:
        buttons.append(types.InlineKeyboardButton(text='>', callback_data=f'BetReset:{player.userId}_{bet+50}'))
    else:
        buttons.append(types.InlineKeyboardButton(text='  ', callback_data=f'@$^'))
    if player.money >= bet + 100:
        buttons.append(types.InlineKeyboardButton(text='>>', callback_data=f'BetReset:{player.userId}_{bet+100}'))
    else:
        buttons.append(types.InlineKeyboardButton(text='  ', callback_data=f'@$^'))
    keyboard.row(*buttons)
    keyboard.add(
        types.InlineKeyboardButton(text='Бросить кости', callback_data=f'BetPlay:{player.userId}_{bet}')
    )
    return keyboard

async def SetBet(call: types.CallbackQuery):
    player = Player.GetPlayer(call.message.chat.id, call.from_user.id)

    if not player:
        await call.answer('Нужно зарегистрироваться для такого')
        return

    if player.money < 50:
        await call.answer('Нужны денюшки для такого')
        return
    
    keyboard = GetBetKeyboard(50, player)
    #TODO: спросить мем у Данича
    text='Все просто как #.\nКидаем кости по очереди, у кого больше - тот и забирает ставку.\nЕсли ничья - остаемся при своем.'

    await call.message.answer_photo(
        photo=open(ROOT / 'static/dice/' / random.choice(os.listdir(ROOT / 'static/dice')), 'rb'),
        caption=text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    await call.answer()
    
async def ResetBet(call: types.CallbackQuery):

    userId, bet = call.data.replace('BetReset:','').split('_')
    userId, bet = int(userId), int(bet)

    if userId != call.from_user.id:
        await call.answer('Это не ваше')
        return

    player = Player.GetPlayer(call.message.chat.id, call.from_user.id)
    keyboard = GetBetKeyboard(bet, player)
    await call.message.edit_reply_markup(
        reply_markup=keyboard
    )

async def PlayBet(call: types.CallbackQuery):
    userId, bet = call.data.replace('BetPlay:','').split('_')
    userId, bet = int(userId), int(bet)

    if userId != call.from_user.id:
        await call.answer('Это не ваше')
        return

    player = Player.GetPlayer(call.message.chat.id, call.from_user.id)

    if player.money < bet:
        await call.answer('Нужны денюшки для такого')
        return
    
    BotThrow = [random.randint(1,6), random.randint(1,6)]
    PlayerThrow = [random.randint(1,6), random.randint(1,6)]

    for i in range(2):
        if PlayerThrow[i] < 6 and random.random() < (1/PlayerThrow[i]) * player.fullLuck:
            PlayerThrow[i]+=1

    for i in range(2):
        if BotThrow[i] < 6 and random.random() < (1/BotThrow[i]) * IBMLuck:
            BotThrow[i]+=1

    text = f'''
Вы бросили кости:
Первый кубик: {PlayerThrow[0]}
Второй кубик: {PlayerThrow[1]}
Сумма: {sum(PlayerThrow)}

ЭйБиЭм посмеялся старым восьмибитным смехом и кинул свои кости:
Первый кубик: {BotThrow[0]}
Второй кубик: {BotThrow[1]}
Сумма: {sum(BotThrow)}

'''
    result = sum(PlayerThrow) - sum(BotThrow)
    if result > 0:
        text+= f'Вы выиграли и забрали банк.\n<b>Получено</b>:\nДеньги: {bet}'
        player.money += bet
    elif result < 0:
        text+= f'Вы проиграли и старый хитрый ЭйБиЭм забирает ваши деньги.\n<b>Потеряно</b>:\nДеньги: {bet}'
        player.money -= bet
    else:
        text+=f'Ничья, все остались при своем...'
    
    
    if player.money >= bet:
        keyboard = GetBetKeyboard(bet, player)
    elif player.money >= 50:
        keyboard = GetBetKeyboard(50, player)
    else:
        keyboard = None
    
    await call.message.edit_caption(
        caption=text,
        parse_mode='HTML',
        reply_markup=keyboard
    )

def register_handlers_dice(dp: Dispatcher):
    dp.register_message_handler(startDiceGame, state=None, commands='dice')
    dp.register_callback_query_handler(SetBet, state=None, regexp='^BetSet:')
    dp.register_callback_query_handler(ResetBet, state=None, regexp='^BetReset:*')
    dp.register_callback_query_handler(PlayBet, state=None, regexp='^BetPlay:*')