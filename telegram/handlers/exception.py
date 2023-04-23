from aiogram.dispatcher import Dispatcher
from aiogram import types

async def errorHandler(update: types.Update, exception: Exception) -> bool:
    
    print( exception.__str__() )
    return True


def register_handlers_exception(dp: Dispatcher):
    dp.register_errors_handler(errorHandler)
