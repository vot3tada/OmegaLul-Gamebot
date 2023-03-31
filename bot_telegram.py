from aiogram.utils import executor
from utils.create_bot import dp
import handlers
import utils.JsonParser as JsonParser
from utils.scheduler import scheduler
import Classes.Player as Player

async def Startup(dp):
    Player.Players = JsonParser.LoadUsers()
    print()

async def Shutdown(dp):
    scheduler.shutdown()
    JsonParser.SaveUsers()
    

handlers.register_handlers(dp)
executor.start_polling(dp, skip_updates = True, on_startup=Startup ,on_shutdown=Shutdown)