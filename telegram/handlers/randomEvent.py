import Classes.Player as Player
import Classes.Good as Item
import random
import Classes.History as History
from utils.create_bot import bot, dp
from utils.scheduler import scheduler
import aiogram


async def RandomEvent(chatId: int):
    try:
        players:list[Player.Player] = Player.GetAllPlayers(chatId)
        events: list[Item.Good] = Item.GetRandomEventItems()
        player = random.choice(players)
        event = random.choice(events)
        player.BuffByItem(event)
        history = History.GetHistory(player.chatId, player.userId)
        match event.effects[0]['property']:
            case 'exp':
                history.UpdateHistory(totalExp=event.effects[0]['value'])
            case 'money':
                if event.effects[0]['value'] > 0:
                    history.UpdateHistory(totalMoney=event.effects[0]['value'])
        await bot.send_message(chat_id=chatId, text=f'{player.name} попал под событие:\n<b>{event.name}</b>\n{event.description}', parse_mode='HTML')
    except aiogram.exceptions.ChatNotFound:
        print(f'chat: {chatId} removed')
        scheduler.remove_job(f'RE:{chatId}')
    except aiogram.utils.exceptions.Unauthorized:
        print(f'chat: {chatId} removed')
        scheduler.remove_job(f'RE:{chatId}')
    
def AddRandomEventInChat(chatId: int):
    job = scheduler.get_job(f'RE:{chatId}')
    if (job == None):
        scheduler.add_job(RandomEvent, trigger='interval', seconds=86400, args=[chatId], coalesce=True, id=f'RE:{chatId}') 