from . import user, registration, shop, talk, fight
from aiogram.dispatcher import Dispatcher

def register_handlers(dp : Dispatcher):
    registration.register_handlers_registration(dp)
    fight.register_fight_handlers(dp)
    shop.register_handlers_shop(dp)
    talk.register_handlers_talk(dp)
    user.register_handlers_user(dp)
    
