from aiogram.utils import executor
from utils.create_bot import dp
import handlers
from utils.scheduler import scheduler

async def StartUp(dp):
    scheduler.print_jobs()

async def Shutdown(dp):
    scheduler.shutdown()

handlers.register_handlers(dp)
executor.start_polling(dp, skip_updates = True, on_startup=StartUp ,on_shutdown=Shutdown)