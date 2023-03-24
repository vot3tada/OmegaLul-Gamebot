from aiogram.utils import executor
from create_bot import dp
from aiogram import types

users = dict()

from handlers import registration

registration.register_handlers_registration(dp)



executor.start_polling(dp, skip_updates = True)