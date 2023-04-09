from aiogram.dispatcher import Dispatcher
from aiogram import types

async def getCommands(message: types.Message):
    await message.reply(
        text =
        """<b>Команды игрового Омехалюля</b>:

        <i>Персонаж</i>:
        /registration - регистрируем лучшего персонажа
        /cancel - отменить регистрацию
        /avatar - посмотреть свой профиль
        /inventory - посмотреть и использовать вещи

        <i>Сражения</i>:
        /duel - вызвать бойца на дуэль
        /duel_accept - принять дуэль
        /duel_refuse - отменить дуэль

        <i>Работенка</i>:
        /work - показать список работ
        /work_escape - досрочно убежать с работы

        <i>Мероприятия</i>:
        *
        *
        *

        <i>Другие</i>:
        /shop - вызвать магазинчик для закупа""",
        parse_mode='HTMl'
    )

def register_handlers_info(dp: Dispatcher):
    dp.register_message_handler(getCommands, commands='help', state='*')
