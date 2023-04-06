from handlers import avatar, registration, shop, fight, work, event, item, info
from aiogram.dispatcher import Dispatcher

def register_handlers(dp : Dispatcher):
    registration.register_handlers_registration(dp)
    fight.register_fight_handlers(dp)
    shop.register_handlers_shop(dp)
    item.register_handlers_item(dp)
    work.register_handlers_work(dp)
    avatar.register_handlers_user(dp)
    event.register_handlers_registration(dp)
    info.register_handlers_info(dp)

    
