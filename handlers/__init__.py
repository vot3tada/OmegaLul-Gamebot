from . import fight, registration
from aiogram.dispatcher import Dispatcher

def register_handlers(dp : Dispatcher):
    registration.register_handlers_registration(dp)
    fight.register_fight_handlers(dp)
    
