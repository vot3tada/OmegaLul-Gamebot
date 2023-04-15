import Classes.Player as Player
import Classes.Achievement as Achievement
from utils.create_bot import bot, dp

async def SendAchievement(chatId: int, userId: int, achievementsId: list[int]):
    for i in achievementsId:
        achievement = Achievement.GetAchievement(i)
        player = Player.GetPlayer(chatId, userId)
        photo = open('./static/achiv/'+achievement.image,'rb')
        await bot.send_photo(chat_id=chatId, caption=f'<b>{player.name}</b> зарабатывает достижение:\n<b>{achievement.name}</b>\n{achievement.description}',
            photo=photo, parse_mode='HTML')