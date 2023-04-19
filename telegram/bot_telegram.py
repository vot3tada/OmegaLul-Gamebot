from aiogram.utils import executor
from utils.create_bot import dp
import handlers
from utils.scheduler import scheduler
from pathlib import Path
import sys
import os

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0] 
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT)) 
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))

async def StartUp(dp):
    scheduler.print_jobs()

async def Shutdown(dp):
    scheduler.shutdown()

handlers.register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True, on_startup=StartUp ,on_shutdown=Shutdown)