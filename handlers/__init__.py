from handlers import avatar, registration, shop, fight, talk, work, event, item, info, task, collector, quiz, raid, achievement
from aiogram.dispatcher import Dispatcher

def register_handlers(dp : Dispatcher):
    registration.register_handlers_registration(dp)
    fight.register_fight_handlers(dp)
    shop.register_handlers_shop(dp)
    item.register_handlers_item(dp)
    work.register_handlers_work(dp)
    task.register_handlers_task(dp)
    avatar.register_handlers_user(dp)
    collector.register_handlers_collector(dp)
    event.register_handlers_registration(dp)
    info.register_handlers_info(dp)
    talk.register_handlers_talk(dp)
    quiz.register_handlers_quiz(dp)
    raid.register_handlers_raid(dp)
    achievement.register_handlers_achievement(dp)

    
