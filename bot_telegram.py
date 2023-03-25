from aiogram.utils import executor
from create_bot import dp
import handlers
from handlers.registration import users
import pickle

async def LoadUsers(dp):
    with open("users.pkl", "rb") as file:
        handlers.registration.users = pickle.load(file)

handlers.register_handlers(dp)
executor.start_polling(dp, skip_updates = True, on_startup=LoadUsers)