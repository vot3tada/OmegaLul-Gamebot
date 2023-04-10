from aiogram.dispatcher import Dispatcher
from emoji import emojize
from aiogram import types
import os, random

async def welcomeMessage(message: types.Message):

    text = f'''<b>Приветсвую тебя!</b>

Я - <b>Омехалюль</b>, игровой бот в стиле нейронного стимпанка

Добавляй меня в свой чат к друзьям, давай админку и вместе вы сможете:

{emojize(':man_construction_worker:')} <i>Создать своего аватара-инженера</i>. Прифотошопьте свое лицо с заранее заготовленным инженерам и радуйте свой глаз <i>великолепным</i> дипфейсом.

{emojize(':crossed_swords:')} <i>Устраивать дуэли с другими инженерами</i>. Ультуйте, защищайтесь и обыгрывайте своего противника за награды.

{emojize(':man_lifting_weights:')} <i>Выполнять задания других инженеров и создавать свои</i>. Словно ведьмак или авантюрист вы будете выполнять задания даже из реального мира.

{emojize(':office_building:')} <i>Ходить на работу</i>. Пока вы сами батрачите отправьте своего инженера работать тоже, чтобы неповадно было.

{emojize(':party_popper:')}  <i>Организовывать мероприятия</i>. Перенесите совещания или сбор в курилке прямо сюда и получите награды и напоминалки о собраниях.

{emojize(':sports_medal:')} <i>Участвовать в квизах</i>. Быстрее других отвечайте на вопросы и получайте награду как чемпион зверей и гиков.

{emojize(':ogre:')} <i>Собирать рейды на босса</i>. Объединяйтесь в другими инженерами для того чтобы повалить ежедневного босса качалки.

{emojize(':mechanical_arm:')} Прокачивайтесь, тратьте деньги на расходники, получайте амуницию с боссов и получайте ачивки. Станьте инженером мессяца!'''

    await message.answer(text=text, parse_mode='HTML')

async def getCommands(message: types.Message):
    await message.reply_photo(
        caption =
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
        parse_mode='HTMl',
        photo=open('./static/info/' + random.choice(os.listdir('./static/info')) ,'rb')
    )

def register_handlers_info(dp: Dispatcher):
    dp.register_message_handler(getCommands, commands='help', state='*')
    dp.register_message_handler(welcomeMessage, commands='start', state=None)
