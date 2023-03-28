from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from utils.scheduler import scheduler
from Classes.Player import Players, Player
from Classes.Work import Works

class FSMWork(StatesGroup):
    work=State()

async def work_info(message : types.Message):
    work_text = 'Хотите отправить вашего работягу по вашим стопам ?\nГде будем батрачить ?\n'
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(Works)):
        work_text += f'{i}) {Works[i].name} (нужен уровень: {Works[i].levelRequired})\nОпыт: {Works[i].expReward} Деньги: {Works[i].moneyReward}\n\n'
        keyboard.add(types.InlineKeyboardButton(text=Works[i].name, callback_data=f"work:{i}"))
    work_text += 'Время работы: 2 часика'
    await message.answer(work_text, reply_markup=keyboard)


async def work_start(call: types.CallbackQuery, state : FSMContext):
    if str(call.from_user.id) not in Players:
        await call.message.reply('Нужно зарегаться для такого')
        return
    user = Players[str(call.from_user.id)]
    work_id = call.data.replace('work:','')
    try:
        work_id = int(work_id)
        work = Works[work_id]
    except:
        await call.message.reply('Что то ты не то нажал')
        return
    
    scheduler.add_job(work_complete, trigger='interval', seconds=5, args=[call.message, f'w_{call.from_user.id}', state, user], coalesce=False, id=f'w_{call.from_user.id}')

    await FSMWork.work.set()
    photo = open(user.photo, 'rb')
    await call.message.reply_photo(photo=photo,caption=f'{user.name} отправился батрачить...')
    await call.answer()

async def work_complete(message: types.Message, id : str, state : FSMContext, user : Player):
    if await state.get_state() == 'FSMWork:work':
        await message.answer(f"{user.name} вернулся с работенки")
        await state.finish()
    scheduler.remove_job(id)
    return

async def work_end(message: types.CallbackQuery, state : FSMContext):
    await state.finish()
    await message.reply('Вы в страхе сбежали с работы')

def register_handlers_work(dp: Dispatcher):
    dp.register_message_handler(work_info, state=None, regexp='^На работу$')
    dp.register_callback_query_handler(work_start, state=None, regexp='^work:*')
    dp.register_message_handler(work_end, state=FSMWork.work, regexp="^Убежать с работы$")