import aiogram
import Classes.Player as Player
from pathlib import Path
import Classes.Git as Git
from utils.scheduler import scheduler
from utils.create_bot import bot
import handlers.achievement as Achievement
import random
import os

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

def GitFormula(git: Git.GitHistory) -> int:
    return (
        git.ApprovedMergeRequests * 0.2 +
        git.OpenedMergeRequests * 0.2 + 
        git.AcceptedMergeRequests * 0.2 +
        git.PushedCommits * 0.1
    )

async def AddGitInChat(chatId: int):
    players = Player.GetAllPlayers(chatId)
    job = scheduler.get_job(f'gitBoard:{chatId}')
    if len(players) and not job:
        scheduler.add_job(SendGit, trigger='cron', day_of_week='mon-fri', hour=18, minute=55, args=[chatId], id=f'gitBoard:{chatId}')

async def SendGit(chatId: int):
    text = '<b>!Лучшие рабочие GitLab\'a!</b>\nВот они, с нулевого индекса...\n\n'
    players:list[Player.Player] = Player.GetAllPlayers(chatId)
    gits:list[Git.GitHistory] = Git.GetChatGit(chatId)
    
    playerGit: list[(Git.GitHistory, Player.Player)] = []

    for git in gits:
        playerGit.append(
            (git, next((x for x in players if x.userId == git.userId), None))
        )

    playerGit.sort(key = lambda x: GitFormula(x[0]))

    for history, player in playerGit:
        history: Git.GitHistory
        player: Player.Player
        Achievement.AddHistory(player.chatId, player.userId, totalCommits=history.PushedCommits, totalMerges=history.AcceptedMergeRequests)

    for history, player in playerGit[:4]:
        history: Git.GitHistory
        player: Player.Player
        score = round(GitFormula(history),2)
        exp = round(score * 1.5)
        player.exp += exp
        Achievement.AddHistory(player.chatId, player.userId, totalExp=exp)
        text += f"""
        <i>{player.name}</i>
                Создал merge request: {history.ApprovedMergeRequests}
                Одобрил merge request: {history.OpenedMergeRequests}
                Слил ветку: {history.AcceptedMergeRequests}
                Запушил commit: {history.PushedCommits}

                Очки кодерского рейтинга: {score}
                <b>Получено</b>: Опыт {exp}
                """
    try:
        await bot.send_photo(
            chatId,
            photo=open(ROOT / 'static/gitBoard/' / random.choice(os.listdir(ROOT / 'static/gitBoard')) ,'rb'),
            caption=text,
            parse_mode='HTML'
        )
    except aiogram.exceptions.ChatNotFound:
        print(f'chat: {chatId} removed')
        scheduler.remove_job(f'gitBoard:{chatId}')
    except aiogram.utils.exceptions.Unauthorized:
        print(f'chat: {chatId} removed')
        scheduler.remove_job(f'gitBoard:{chatId}')


