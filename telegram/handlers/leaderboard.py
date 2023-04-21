from utils.scheduler import scheduler
import Classes.Player as Player
import Classes.History as History
from utils.create_bot import bot
import aiogram
from pathlib import Path
import os
import random

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

def LeaderFormula(his: History.History) -> int:
    return (
        his.totalMoney        * 0.1  +
        his.totalExp          * 0.1  +
        his.totalQuestions    * 0.12 +
        his.totalFights       * 0.15 +
        his.totalWinFights    * 0.18 +
        his.totalWinBoss      * 0.2  +
        his.totalItem         * 0.1  +
        his.totalTakenTasks   * 0.1  +
        his.totalEndedTasks   * 0.12 +
        his.totalFallTasks    * -0.1 +
        his.totalWinCollector * 0.19 +
        his.totalCreateEvent  * 0.12 +
        his.totalEnterEvent   * 0.1  +
        his.totalKickEvent    * 0.05 +
        his.totalLeaveFights  * -0.1
    )


def AddLeaderBoardInChat(chatId: int):#Сделать каждое воскресенье
    players = Player.GetAllPlayers(chatId)
    job = scheduler.get_job(f'leaderboard:{chatId}')
    if len(players) and not job:
        scheduler.add_job(SendLeaderBoard, trigger='interval', weeks=1, args=[chatId], id=f'leaderboard:{chatId}')


async def SendLeaderBoard(chatId: int):
    text = '<b>!Лучшие игроки недели!</b>\nВот они, слева направо...\n\n'

    players:list[Player.Player] = Player.GetAllPlayers(chatId)
    playerAndHistory: list[Player.Player, History.History] = []
    for player in players:
        playerAndHistory.append(
            [player, History.GetHistory(chatId, player.userId)]
        )

    playerAndHistory.sort(key= lambda x: LeaderFormula(x[1]))

    for player, history in playerAndHistory[:10]:
        text += f'    <i>{player.name}</i>\n        Очки социального рейтинга: {round(LeaderFormula(history),2)}\n'
    text+='\nПроявляйте бОльшую активность, механики!!'
    try:
        await bot.send_photo(
            chatId,
            photo=open(ROOT / 'static/leaderboard/' / random.choice(os.listdir(ROOT / 'static/leaderboard')) ,'rb'),
            caption=text,
            parse_mode='HTML'
        )
    except aiogram.exceptions.ChatNotFound:
        print(f'chat: {chatId} removed')
        scheduler.remove_job(f'leaderboard:{chatId}')
    except aiogram.utils.exceptions.Unauthorized:
        print(f'chat: {chatId} removed')
        scheduler.remove_job(f'leaderboard:{chatId}')


async def GetLeaderBoard(message: types.Message):#????? Почему 
    await SendLeaderBoard(message.chat.id)

def register_handlers_leaderboard(dp: Dispatcher):
    dp.register_message_handler(GetLeaderBoard, commands='leader_board', state=None)
