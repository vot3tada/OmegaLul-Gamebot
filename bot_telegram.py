from aiogram.utils import executor
from create_bot import dp
import handlers

users = handlers.registration.users

handlers.register_handlers(dp)

executor.start_polling(dp, skip_updates = True)