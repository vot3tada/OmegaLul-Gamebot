from aiogram.utils import executor
from create_bot import dp
import handlers
from handlers.registration import users
from scheduler import scheduler
import pickle

async def LoadUsers(dp):
    with open("users.pkl", "rb") as file:
        handlers.registration.users = pickle.load(file)

async def Shutdown(dp):
    scheduler.shutdown()
    with open("users.pkl", "wb") as file:
        pickle.dump(users, file)

handlers.register_handlers(dp)
executor.start_polling(dp, skip_updates = True, on_startup=LoadUsers, on_shutdown=Shutdown)