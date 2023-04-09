from aiogram.dispatcher import Dispatcher
from aiogram import types

async def getCommands(message: types.Message):
    await message.reply(
        text=
        """
        Команды игрового Омехалюля:
        Персонаж:
        /registration - регистрируем лучшего персонажа
        /cancel - отменить регистрацию
        /avatar - посмотреть свой профиль
        /inventory - посмотреть и использовать вещи

        Сражения:
        /duel - вызвать бойца на дуэль
        /duel_accept - принять дуэль
        /duel_refuse - отменить дуэль

        Работенка:
        /work - показать список работ
        /work_escape - досрочно убежать с работы

        Мероприятия:
        *
        *
        *

        Другие:
        /shop - вызвать магазинчик для закупа
        """
    )

def register_handlers_info(dp: Dispatcher):
    dp.register_message_handler(getCommands, commands='help', state='*')
