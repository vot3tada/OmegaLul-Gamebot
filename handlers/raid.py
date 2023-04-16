from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import Classes.Raid as Raid
from utils.scheduler import scheduler
import os, random
import Classes.Player as Player
from utils.create_bot import dp, bot

class RaidState(StatesGroup):
    awaiting = State()
    ready = State()
    attack = State()

async def getRaidsList(message: types.Message):

    boss: Raid.Boss = Raid.GetBosses()[0]
    text = f'''
            <b>{boss.name}</b>
            Здоровье: {boss.hp}
            Награда:
                Деньги: {boss.moneyReward}
                Опыт: {boss.expReward}
        '''
    keyboard = types.InlineKeyboardMarkup()
    buttons: list[types.InlineKeyboardButton] = []
    buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
    if len(Raid.GetBosses()) > 1:
        buttons.append( types.InlineKeyboardButton(text='След. ', callback_data=f'bossList:{message.chat.id}_{message.from_user.id}_1'))
    else:
        buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
    keyboard.row(*buttons)
    keyboard.add(
        types.InlineKeyboardButton(text=f'Собрать команду на этого босса', callback_data=f'startRecr:{message.chat.id}_{message.from_user.id}_{boss.id}')
    )

    await message.answer_photo(
        photo= open(boss.photo, 'rb'),
        caption=text,
        reply_markup= keyboard,
        parse_mode='HTML'
    )

async def pageRaidsList(call: types.CallbackQuery):

    chatId, userId, page = call.data.replace("bossList:",'').split('_')
    if call.message.chat.id != int(chatId) or call.from_user.id != int(userId):
        await call.answer('Это не ваш список')
        return
    try:
        page = int(page)
    except:
        await call.answer('Номер страницы неверен')
        return

    boss: Raid.Boss = Raid.GetBosses()[page]
    text = f'''
            <b>{boss.name}</b>
            Здоровье: {boss.hp}
            Награда:
                Деньги: {boss.moneyReward}
                Опыт: {boss.expReward}
        '''
    keyboard = types.InlineKeyboardMarkup()
    buttons: list[types.InlineKeyboardButton] = []
    if page:
        buttons.append( types.InlineKeyboardButton(text='Пред. ', callback_data=f'bossList:{call.message.chat.id}_{call.from_user.id}_{page-1}'))
    else:
        buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
    if len(Raid.GetBosses()) > page+1:
        buttons.append( types.InlineKeyboardButton(text='След. ', callback_data=f'bossList:{call.message.chat.id}_{call.from_user.id}_{page+1}'))
    else:
        buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
    keyboard.row(*buttons)
    keyboard.add(
        types.InlineKeyboardButton(text=f'Собрать команду на этого босса', callback_data=f'startRecr:{call.message.chat.id}_{call.from_user.id}_{boss.id}')
    )
    media = types.input_media.InputMediaPhoto(media=types.InputFile(boss.photo), caption=text, parse_mode='HTML')
    await call.message.edit_media(
        media=media,
        reply_markup= keyboard
    )
    await call.answer()

async def startRecr(call: types.CallbackQuery):

    chatId, userId, bossId = call.data.replace("startRecr:",'').split('_')
    try:
        chatId, userId, bossId = int(chatId), int(userId), int(bossId)
    except:
        await call.answer()
        return
    if call.message.chat.id != int(chatId) or call.from_user.id != int(userId):
        await call.answer('Это не ваш список')
        return
    if not Player.GetPlayer(chatId, userId):
        await call.answer('Нужно зарегистрироваться для такого')
        return
    try:
        bossId = int(bossId)
        
    except:
        await call.answer('Номер босса неверен')
        return
    
    boss = Raid.GetBoss(bossId)

    if not boss:
        await call.answer('Номер босса неверен')
        return

    chatRaid = Raid.GetChatRaid(call.message.chat.id)
    if chatRaid:
        await call.answer('В чате уже проходит рейд на босса')
        return
    
    Raid.StartRaidInChat(chatId, bossId, userId)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text='Присоединиться к походу',
            callback_data=f'enterRaid:{call.message.chat.id}_{bossId}'
        )
    )
    
    await RaidState.awaiting.set()

    scheduler.add_job(endRecr, jobstore='local' ,trigger='interval',minutes=2, args=[chatId], id=f'raidRecr:{chatId}')

    await call.message.answer_photo(
        photo=open('./static/raidRecr/' + random.choice(os.listdir('./static/raidRecr')), 'rb'),
        parse_mode='HTML',
        caption=f'''
<b>ВНИМАНИЕ</b>
Ведется набор команды для похода на босса:
{boss.name}
Присоединяйтесь в битве!
Покажите свою честь, механики!
<i>Время записи - две минуты</i>
        ''',
        reply_markup=keyboard
    )
    await call.answer()

async def enterToRaid(call: types.CallbackQuery):

    chatId, bossId = call.data.replace("enterRaid:",'').split('_')
    try:
        chatId, bossId = int(chatId), int(bossId)
    except:
        await call.answer('Номер чата неверен')
        return
    
    if chatId != call.message.chat.id:
        await call.answer('Чаты несовпадают')
        return

    player: Player.Player = Player.GetPlayer(chatId, call.from_user.id)
    if not player:
        await call.answer('Нужно зарегистрироваться для такого')
        return

    chatRaid = Raid.GetChatRaid(chatId)
    if not chatRaid:
        await call.answer('В данном чате рейд не проходит')
        return
    
    if chatRaid.boss.id != bossId:
        await call.answer('В данном чате проходит другой рейд')
        return
    
    if chatRaid.GetPlayer(player):
        await call.answer('Вы уже в рейде')
        return

    chatRaid.EnterToRaid(player)
    await RaidState.awaiting.set()
    await call.message.answer(f'{player.name} присоединился к рейду!')
    await call.answer()

async def leaveRaid(message: types.Message, state: FSMContext):
    player = Player.GetPlayer(message.chat.id, message.from_user.id)
    if not player:
        await message.answer('Нужно зарегистрироваться для такого')
        return
    chatRaid = Raid.GetChatRaid(message.chat.id)
    if not chatRaid:
        await message.answer('В данном чате рейд не проходит')
        return
    
    if not chatRaid.GetPlayer(player):
        await message.answer('Вы не состоите в рейде')
        return
    
    left = chatRaid.LeaveFromRaid(player)
    await message.answer(f'{player.name} сбежал с рейда...')
    await state.finish()
    if not left:
        Raid.EndRaidInChat(chatRaid)
        await message.answer(f'Все сбежали с рейда, он окончен...')

    
async def instantEndRecr(message: types.Message):

    chatRaid = Raid.GetChatRaid(message.chat.id)
    if not chatRaid:
        await message.reply('В данном чате рейд не проходит')
        return
    if chatRaid.players[0].userId != message.from_user.id:
        await message.reply('Вы не лидер группы')
        return
    await endRecr(chatId=chatRaid.chatId)
    

async def endRecr(chatId: int):
    
    chatRaid = Raid.GetChatRaid(chatId)
    scheduler.remove_job(f'raidRecr:{chatId}')
    if chatRaid:

        if len(chatRaid.players) > 1:
            for player in chatRaid.players:
                st: FSMContext = dp.current_state(chat=player.chatId, user=player.userId)
                await st.set_state(RaidState.ready)
            await bot.send_message(chat_id=chatId, text='НАЧИНАЕМ РЕЙД!')
        else:
            await bot.send_message(chat_id=chatId, text='Один в поле не войн, рейд не начат...')
            for player in chatRaid.players:
                st: FSMContext = dp.current_state(chat=player.chatId, user=player.userId)
                await st.set_state(None)
                Raid.EndRaidInChat(chatRaid)


def register_handlers_raid(dp: Dispatcher):
    dp.register_message_handler(getRaidsList, commands='raid', state=None)
    dp.register_callback_query_handler(pageRaidsList, state=None, regexp='^bossList:*')
    dp.register_callback_query_handler(startRecr, state=None, regexp='^startRecr:*')
    dp.register_callback_query_handler(enterToRaid, state=[None, RaidState.awaiting], regexp='^enterRaid:*')
    dp.register_message_handler(leaveRaid, state=RaidState.awaiting, commands='raid_leave')
    dp.register_message_handler(instantEndRecr, state=RaidState.awaiting, commands='raid_endRecr')
