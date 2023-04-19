from aiogram.utils import executor
from telegram.utils.create_bot import dp
import telegram.handlers as handlers
from telegram.utils.scheduler import scheduler

async def StartUp(dp):
    scheduler.print_jobs()

async def Shutdown(dp):
    scheduler.shutdown()

handlers.register_handlers(dp)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True, on_startup=StartUp ,on_shutdown=Shutdown)