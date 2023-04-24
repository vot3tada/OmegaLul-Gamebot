from aiogram.dispatcher import Dispatcher
from aiogram import types
import os, random
from pathlib import Path
from handlers.fight import HPCut
from handlers.raid import bossHPCut
from handlers.registration import reRegMoney
from handlers.work import workTime
from utils import ParseSeconds

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]


async def welcomeMessage(message: types.Message):
    text = f'''<b>Приветсвую тебя!</b>

Я - <b>Механобот</b>, игровой бот в стиле нейронного стимпанка

Добавляй меня в свой чат к друзьям, давай админку и вместе вы сможете:

👷‍♂️ <i>Создать своего аватара-инженера</i>. 

⚔ <i>Устраивать дуэли с другими инженерами</i>.

🏋️‍♀️ <i>Выполнять задания других инженеров и создавать свои</i>.

🏢 <i>Ходить на работу</i>.

🎉  <i>Организовывать мероприятия</i>.

🏅 <i>Участвовать в квизах</i>.

👹 <i>Собирать рейды на босса</i>.

🦾 Прокачивайтесь, тратьте деньги на расходники, получайте амуницию с боссов и получайте ачивки. Станьте инженером мессяца!'''

    await message.answer_photo(caption=text, parse_mode='HTML',
                         photo=open(ROOT / 'static/start/OmegaHello.jpg', 'rb'))
    

helpSections: dict[str, str] = {
    "Общий": '<b>Какой разел Механобота вас интересует?</b>',
    "Персонаж": f"""
<b>Персонаж</b>
Команды:
/registration - создать персонажа
/cancel - отмена регистрации
/avatar_change - сменить персонажа
/avatar - посмотреть персонажа, баффы и хар-ки
/inventory - посмотреть инвентарь

Смена персонажа будет стоит вам {reRegMoney}.""",
    "Дуэль": f"""
<b>Дуэли</b>
Команды:
/duel - ответьте на сообщение инженера этой командой чтобы вызвать на дуэль
/duel_accept - подтвердить дуэль
/duel_refuse - отказаться от дуэли 

Ваше максимальное здоровье в бою зависит от здоровья вашего персонажа.
При любом окончании битвы оба бойца тратят {HPCut} хп за проведения схватки.
Вы можете начать бой при любом хп, кроме нулевого.
Чем меньше у вас хп - тем труднее победить, но лучше награда!
Также не забывайте что бездействие приведет к поражению...""",
    "Задания":f"""
    <b>Задания</b>
Команды:
/task - посмотреть список свободных заданий 
/task_given - посмотреть список своих выставленных заданий
/task_taken - посмотреть список взятых заданий
/task_take [номер] - взять задание под данным номером
/task_add - добавить свое задание на доску
/task_cancel - отменить создание 

На доске обьявлений каждый может выставлять свое любое задание, назначать за него награду и время выполнения.
Награду вы платите из своего кармана, админы чата платят в два раза меньше. 

Взятое задание пропадает с доски, отказаться от него можно в своем списке. 
<b>Помните</b>, что отмена задания, дедлайн которого прошел уже на треть,будет наказана, 
за вами придет <i>Он</i>...

Зачесть выполненое задание вам может человек, выставивший его, обратитесь к нему. 
Также за треть времени до конца задания вам придет напоминалка в личку, так что включите МеханоБота для себя!
""",
    "Работа": f"""
    <b>Работа</b>
Команды:
/work - посмотреть возможные работы
/work_escape - сбежать досрочно с работы

Пока вы сами работаете, вы можете отправить своего механика тоже трудиться. 
Время работы: {ParseSeconds(workTime)}
Во время работы ваш персонаж не может совершать другие действия.
Сбегание досрочно с работы не дает вам награды.
""",
    "Мероприятия": f"""
    <b>Мероприятия</b>
Команды:
/event - посмотреть запланированные эвенты
/event_create - запланировать мероприятие
/event_cancel - отменить планирование мероприятия
/event_delete - удалить запланированное мероприятие
/event_end - законить регистрацию на мероприятие
/event_kick - выгнать человека с мероприятия

Переносите мероприятия из реальности сюда.
За присутсвие на мероприятии вы получите награды, но не хальтурьте, админы могут выгнать вас на "мнимое" присутствие.

Также вы получите упоминание за час и при начале мероприятия в личку, так что включите МеханоБота для себя!
""",
    "Рейды": f"""
    <b>Рейды</b>
Команды:
/raid - посмотреть список боссов, на которых можно устроить похож
/raid_leave - покинуть рейд на стадии набора

Рейды представляют собой групповые бои против одного мощного врага.
В бою может присутствовать от двух до 15 человек. 

При любом окончании битвы все бойцы тратят {bossHPCut} хп за проведения схватки.
После победы награду за босса делят все участники схватки, доля зависит от внесенного боссу урона.

Также между живыми бойцами будет разыгран один трофей с босса в виде предмета. 
""",
    "Викторины": f"""
    <b>Викторины</b>
Команды:
/quiz - посмотреть список доступных викторин
/quiz_enter - присоединиться к викторине
/quiz_leave - покинуть викторину на любой стадии

Устраивайте викторины, отвечайте на случайные вопросы из списка первым и получайте награды.
""",
    "Ачивки": f"""
Команды:
/achiv - посмотреть список своих ачивок

Все ваши успехи и поражения Омехалюль отслеживает и выдает вам ачивки за это.
Условия ачивок можно посмотреть только после их выполнения.""",
    "Диалог с МеханоБотом": f"""
    <b>Диалог</b>
Команды:
/talk - начать диалог с МеханоБотом.

После введения команды напишите боту любой вопрос.
Разговорный модуль МеханоБот основан на подключении ChatGPT.""",
    "Игра в кости": f"""
    <b>Игра в кости</b>
Команды:
/dice - начать игру в кости

Сыграй в простую игру со стариком ЭйБиЭм'ом.
И пусть ваша <i>удача</i> поможет вам.
Интересно, какая удача у этого хитрого деда ..?
"""
}
   


async def getHelp(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    for helpSection in list(helpSections.keys())[1:]:
        keyboard.add(
            types.InlineKeyboardButton(text=helpSection, callback_data=f'help:{helpSection}_{message.from_user.id}')
        )
    await message.reply_photo(
        caption='<b>Какой раздел Механобота вас интересует?</b>',
        parse_mode='HTMl',
        photo=open(ROOT / 'static/info/' / random.choice(os.listdir(ROOT / 'static/info')), 'rb'),
        reply_markup=keyboard
    )

async def getHelpSection(call: types.CallbackQuery):
    section, userId = call.data.replace('help:','').split('_')
    userId = int(userId)
    if call.from_user.id != userId:
        await call.answer('Это не ваше')
        return
    keyboard = types.InlineKeyboardMarkup()
    if section == 'Общий':
        for helpSection in list(helpSections.keys())[1:]:
            keyboard.add(
                types.InlineKeyboardButton(text=helpSection, callback_data=f'help:{helpSection}_{call.from_user.id}')
            )   
    else:
        keyboard.add(
            types.InlineKeyboardButton(text='Вернуться к выбору раздела', callback_data=f'help:Общий_{call.from_user.id}')
        )
    media = types.input_media.InputMediaPhoto(
        media=types.InputFile(ROOT / 'static/info/' / random.choice(os.listdir(ROOT / 'static/info'))), 
        caption=helpSections[section], 
        parse_mode='HTML')
    await call.message.edit_media(
        media=media,
        reply_markup=keyboard
    )


def register_handlers_info(dp: Dispatcher):
    dp.register_message_handler(getHelp, commands='help', state='*')
    dp.register_message_handler(welcomeMessage, commands='start', state=None)
    dp.register_callback_query_handler(getHelpSection, regexp='^help:', state='*')
