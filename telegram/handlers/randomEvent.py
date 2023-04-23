import Classes.Player as Player
import Classes.Good as Item
import random
import Classes.History as History
from utils.create_bot import bot, dp
from utils.scheduler import scheduler
import aiogram
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

async def RandomEvent(chatId: int):
    players:list[Player.Player] = Player.GetAllPlayers(chatId)
    events: list[Item.Good] = Item.GetRandomEventItems()
    player = random.choice(players)
    event = random.choice(events)
    player.BuffByItem(event)
    history = History.GetHistory(player.chatId, player.userId)
    if event.effects[0]['property'] == 'exp':
            history.UpdateHistory(totalExp=event.effects[0]['value'])
    elif event.effects[0]['property'] == 'money':
        if event.effects[0]['value'] > 0:
            history.UpdateHistory(totalMoney=event.effects[0]['value'])
    try:
        await bot.send_photo(chat_id=chatId, 
                             photo=open(ROOT / 'static/randomEvent' / (str(event.id) + '.jpg') ,'rb'),
                             caption=f'{player.name} попал под событие:\n<b>{event.name}</b>\n{event.description}', parse_mode='HTML')
    except aiogram.exceptions.ChatNotFound:
        print(f'chat: {chatId} removed')
        scheduler.remove_job(f'RE:{chatId}')
    except aiogram.utils.exceptions.Unauthorized:
        print(f'chat: {chatId} removed')
        scheduler.remove_job(f'RE:{chatId}')
    
def AddRandomEventInChat(chatId: int):
    job = scheduler.get_job(f'RE:{chatId}')
    if (job == None):
        scheduler.add_job(RandomEvent, trigger='cron', day_of_week='mon-fri', hour=10, minute=30, args=[chatId], coalesce=True, id=f'RE:{chatId}') 