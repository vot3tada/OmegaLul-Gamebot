from aiogram.dispatcher import Dispatcher
from aiogram import types
import Classes.Player as Player
import Classes.Achievement as Achievement
import Classes.History as History
from utils.create_bot import bot, dp
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

async def AddHistory(chatId: int, userId: int, totalMoney = 0, totalExp = 0, totalQuestions = 0, totalFights = 0, totalWinFights = 0, totalWinBoss = 0,
                       totalItem = 0, totalTakenTasks = 0, totalEndedTasks = 0, totalFallTasks = 0, totalWinCollector = 0,
                         totalCreateEvent = 0, totalEnterEvent = 0, totalKickEvent = 0, totalLeaveFights = 0):
    history = History.GetHistory(chatId, userId)
    await SendAchievement(chatId, userId, history.UpdateHistory(totalMoney, totalExp, totalQuestions, totalFights, totalWinFights, totalWinBoss,
                       totalItem, totalTakenTasks, totalEndedTasks, totalFallTasks, totalWinCollector,
                         totalCreateEvent, totalEnterEvent, totalKickEvent, totalLeaveFights))

async def SendAchievement(chatId: int, userId: int, achievementsId: list[int]):
    for i in achievementsId:
        achievement = Achievement.GetAchievement(i)
        player = Player.GetPlayer(chatId, userId)
        photo = open(ROOT / 'static/achiv/' / achievement.image,'rb')
        await bot.send_photo(chat_id=chatId, caption=f'<b>{player.name}</b> зарабатывает достижение:\n<b>{achievement.name}</b>\n{achievement.description}',
            photo=photo, parse_mode='HTML')

async def GetAchievements(message : types.Message):
    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Нужно зарегаться для такого')
        return
    userAchiv: list[Achievement.UserAchievement] = Achievement.GetUserAchivs(message.chat.id, message.from_user.id)
    if len(userAchiv) == 0:
        await message.reply('У вас нет ачивок😓')
        return
    achievement = Achievement.GetAchievement(userAchiv[0].achId)
    replytext = f'<b>{achievement.name}</b>:\n{achievement.description}\n'
    buttons: list[types.InlineKeyboardButton] = []
    buttons.append(types.InlineKeyboardButton(text=' ', callback_data=f'@$^'))
    if (len(userAchiv) > 1):
        buttons.append(types.InlineKeyboardButton(text='>', callback_data=f'achiv:{message.chat.id}_{message.from_user.id}_1'))
    else:
        buttons.append(types.InlineKeyboardButton(text=' ', callback_data=f'@$^'))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(*buttons)
    await message.answer_photo(
        caption=replytext,
        photo=open(ROOT / 'static/achiv/' /achievement.image, 'rb'),
        reply_markup=keyboard,
        parse_mode='HTML'
    )

async def GetAchievementsPages(call: types.CallbackQuery):
    chatId, userId, page = call.data.replace("achiv:",'').split('_')
    if call.message.chat.id != int(chatId) or call.from_user.id != int(userId):
        await call.answer('Это не ваш список')
        return
    try:
        page = int(page)
    except:
        await call.answer()
        return
    
    
    userAchiv: list[Achievement.UserAchievement] = Achievement.GetUserAchivs(call.message.chat.id, call.from_user.id)

    achievement = Achievement.GetAchievement(userAchiv[page].achId)
    replytext = f'<b>{achievement.name}</b>:\n{achievement.description}\n'

    replytext = f'<b>{achievement.name}</b>:\n{achievement.description}\n'
    buttons: list[types.InlineKeyboardButton] = []
    if (page - 1 < 0):
        buttons.append(types.InlineKeyboardButton(text=' ', callback_data=f'@$^'))
    else:
        buttons.append(types.InlineKeyboardButton(text='<', callback_data=f'achiv:{call.message.chat.id}_{call.from_user.id}_{page - 1}'))
    if (page + 1 < len(userAchiv)):
        buttons.append(types.InlineKeyboardButton(text='>', callback_data=f'achiv:{call.message.chat.id}_{call.from_user.id}_{page + 1}'))
    else:
        buttons.append(types.InlineKeyboardButton(text=' ', callback_data=f'@$^'))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(*buttons)
    media = types.input_media.InputMediaPhoto(media=types.InputFile(ROOT / 'static/achiv/' /achievement.image), caption=replytext, parse_mode='HTML')
    await call.message.edit_media(media, reply_markup=keyboard)


def register_handlers_achievement(dp: Dispatcher):
    dp.register_message_handler(GetAchievements, commands='achiv_list')
    dp.register_callback_query_handler(GetAchievementsPages, regexp='^achiv:*')