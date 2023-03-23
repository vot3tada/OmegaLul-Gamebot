from aiogram.utils import executor
from create_bot import dp



from handlers import registration

registration.register_handlers_registration(dp)



executor.start_polling(dp, skip_updates = True)