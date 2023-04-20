import Classes.Player as Player
import random
from utils.create_bot import bot, dp


async def RandomEvent(chatId: int, userId: int):
    if (random.randint(0,100) < 100):
        player = Player.GetPlayer(chatId, userId)
        events: list[RE.RandomEvent] = RE.GetAllRandomEvents()
        random.shuffle(events)
        event = events[0]
        #player.BuffByItem()
        await bot.send_message(chat_id=chatId, text=f'{player.name}\n<b>{event.name}</b>\n{event.description}', parse_mode='HTML')
        
