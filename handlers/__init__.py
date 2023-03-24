from . import fight
from aiogram.dispatcher import Dispatcher

def register_handlers(dp : Dispatcher):
    fight.register_fight_handlers(dp)