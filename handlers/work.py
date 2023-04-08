from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from utils.scheduler import scheduler
import Classes.Player as Player
import Classes.Work as Work
from utils.create_bot import dp, bot

class FSMWork(StatesGroup):
    work=State()

async def work_info(message : types.Message):
    work_text = 'Хотите отправить вашего работягу по вашим стопам ?\nГде будем батрачить ?\n'
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(Work.Works)):
        work_text += f'{i}) {Work.Works[i].name} (нужен уровень: {Work.Works[i].levelRequired})\nОпыт: {Work.Works[i].expReward} Деньги: {Work.Works[i].moneyReward}\n\n'
        keyboard.add(types.InlineKeyboardButton(text=Work.Works[i].name, callback_data=f"work:{Work.Works[i].id}"))
    work_text += 'Время работы: 2 часика'
    await message.answer(work_text, reply_markup=keyboard)


async def work_start(call: types.CallbackQuery):
    if not Player.FindPlayer(call.message.chat.id, call.from_user.id):
        await call.message.reply('Нужно зарегаться для такого')
        return
    user = Player.GetPlayer(call.message.chat.id, call.from_user.id)
    work_id = call.data.replace('work:','')
    try:
        work_id = int(work_id)
        work = Work.Works[work_id]
    except:
        await call.answer('Что то ты не то нажал')
        return
    if user.level < work.levelRequired:
        await call.answer('Это не ваш уровень')
        return
    scheduler.add_job(work_complete, trigger='interval', seconds=10, args=[user.chatId, user.userId, work.id, call.from_user.username], coalesce=True, id=f'work_{user.chatId}_{user.userId}')
    await FSMWork.work.set()
    photo = open(user.photo, 'rb')
    await call.message.reply_photo(photo=photo,caption=f'{user.name} отправился {work.name}')
    await call.answer()

async def work_complete(chatId: int, userId: int, workId: int, username: str):

    user: Player.Player = Player.GetPlayer(chatId, userId)
    work = Work.Works[workId] 
    state = dp.current_state(chat=chatId, user=userId)

    user.exp += work.expReward 
    user.money += work.moneyReward
    await state.finish()
    scheduler.remove_job(f'work_{user.chatId}_{user.userId}')
    await bot.send_photo(chat_id=chatId,  
                        caption=f"@{username}\n{user.name} вернулся с работенки!\n<b>Получено</b>:\n{work.expReward} опыта\n{work.moneyReward} денег", 
                        photo=open(user.photo,'rb'),
                        parse_mode='HTML')

async def work_end(message: types.Message, state : FSMContext):
    user = Player.GetPlayer(message.chat.id, message.from_user.id)
    await state.finish()
    scheduler.remove_job(f'work_{user.chatId}_{user.userId}')
    await message.reply(f'{user.name} в страхе сбежал(а) с работы')

def register_handlers_work(dp: Dispatcher):
    dp.register_message_handler(work_info, state=None, commands='work')
    dp.register_callback_query_handler(work_start, state=None, regexp='^work:*')
    dp.register_message_handler(work_end, state=FSMWork.work, commands='work_escape')