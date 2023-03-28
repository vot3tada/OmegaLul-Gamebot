from . import user, registration, shop, talk, fight,  work
from aiogram.dispatcher import Dispatcher

def register_handlers(dp : Dispatcher):
    registration.register_handlers_registration(dp)
    fight.register_fight_handlers(dp)
    shop.register_handlers_shop(dp)
    #talk.register_handlers_talk(dp)
    work.register_handlers_work(dp)
    user.register_handlers_user(dp)
    
