from aiogram.utils import executor
from utils.create_bot import dp
import handlers
from Classes.Player import SaveUsers
from utils.scheduler import scheduler


async def Shutdown(dp):
    scheduler.shutdown()
    SaveUsers()
    

handlers.register_handlers(dp)
executor.start_polling(dp, skip_updates = True, on_shutdown=Shutdown)