from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import Classes.Raid as Raid
from utils.scheduler import scheduler
import os, random
import Classes.Player as Player
from utils.create_bot import dp, bot
from Classes.Fighter import *
import handlers.achievement as AchievementHandler
from pathlib import Path
import Classes.Good as Good

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]


class RaidState(StatesGroup):
    awaiting = State()
    ready = State()
    attack = State()
    dead = State()
    runOut = State()
    reward = State()


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
    buttons: list[types.InlineKeyboardButton] = [types.InlineKeyboardButton(text='    ', callback_data=f'@$^')]
    if len(Raid.GetBosses()) > 1:
        buttons.append(types.InlineKeyboardButton(text='След. ',
                                                  callback_data=f'bossList:{message.chat.id}_{message.from_user.id}_1'))
    else:
        buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
    keyboard.row(*buttons)
    keyboard.add(
        types.InlineKeyboardButton(text=f'Собрать команду на этого босса',
                                   callback_data=f'startRecr:{message.chat.id}_{message.from_user.id}_{boss.id}')
    )

    await message.answer_photo(
        photo=open(boss.photo, 'rb'),
        caption=text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )


async def pageRaidsList(call: types.CallbackQuery):
    chatId, userId, page = call.data.replace("bossList:", '').split('_')
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
        buttons.append(types.InlineKeyboardButton(text='Пред. ',
                                                  callback_data=f'bossList:{call.message.chat.id}_{call.from_user.id}_{page - 1}'))
    else:
        buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
    if len(Raid.GetBosses()) > page + 1:
        buttons.append(types.InlineKeyboardButton(text='След. ',
                                                  callback_data=f'bossList:{call.message.chat.id}_{call.from_user.id}_{page + 1}'))
    else:
        buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
    keyboard.row(*buttons)
    keyboard.add(
        types.InlineKeyboardButton(text=f'Собрать команду на этого босса',
                                   callback_data=f'startRecr:{call.message.chat.id}_{call.from_user.id}_{boss.id}')
    )
    media = types.input_media.InputMediaPhoto(media=types.InputFile(boss.photo), caption=text, parse_mode='HTML')
    await call.message.edit_media(
        media=media,
        reply_markup=keyboard
    )
    await call.answer()


async def startRecr(call: types.CallbackQuery):
    chatId, userId, bossId = call.data.replace("startRecr:", '').split('_')
    try:
        chatId, userId, bossId = int(chatId), int(userId), int(bossId)
    except:
        await call.answer()
        return
    if call.message.chat.id != int(chatId) or call.from_user.id != int(userId):
        await call.answer('Это не ваш список')
        return
    player = Player.GetPlayer(chatId, userId)
    if not player:
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

    if player.hp < 15:
        await call.answer('У вас мало здоровья, боец')
        return

    chatRaid = Raid.StartRaidInChat(chatId, bossId, userId)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text='Присоединиться к походу',
            callback_data=f'enterRaid:{chatRaid.id}'
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text='Закончить набор',
            callback_data=f'endRecr:{chatRaid.id}'
        )
    )

    await RaidState.awaiting.set()

    scheduler.add_job(endRecr, jobstore='local', trigger='interval', minutes=2, args=[chatId], id=f'raidRecr:{chatId}')

    message = await call.message.answer_photo(
        photo=open(ROOT / 'static/raidRecr/' / random.choice(os.listdir(ROOT / 'static/raidRecr')), 'rb'),
        parse_mode='HTML',
        caption=f'''
<b>!!ВНИМАНИЕ!!</b>
Ведется набор команды для похода на босса:
<b>{boss.name}</b>
Присоединяйтесь в битве!
Покажите свою честь, механики!
<i>Время записи - две минуты</i>
<i>Количество человек - не больше 15</i>
        ''',
        reply_markup=keyboard
    )
    for i in Player.GetAllPlayers(call.message.chat.id):
        await bot.send_photo(chat_id=i.userId,
                             photo=open(ROOT / 'static/anonce/' / random.choice(os.listdir(ROOT / 'static/anonce')),
                                        'rb'),
                             caption=f'Сейчас в чате <b>{message.chat.full_name}</b> проходит набор в рейд!\nБосс: <b>{boss.name}</b>!\nПрисоединяйтесь!',
                             parse_mode='HTML'
                             )
    await call.answer()


async def enterToRaid(call: types.CallbackQuery):
    chatRaidId = call.data.replace("enterRaid:", '')

    player: Player.Player = Player.GetPlayer(call.message.chat.id, call.from_user.id)
    if not player:
        await call.answer('Нужно зарегистрироваться для такого')
        return

    chatRaid = Raid.GetChatRaid(chatRaidId)
    if not chatRaid:
        await call.answer('В данном чате данный рейд не проходит')
        return

    if player.hp < 15:
        await call.answer('У вас мало здоровья, боец')
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
    chatRaid = Raid.GetChatRaidByChat(message.chat.id)
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


async def instantEndRecr(call: types.CallbackQuery):
    chatRaidId = call.data.replace('endRecr:', '')

    chatRaid = Raid.GetChatRaid(chatRaidId)
    if not chatRaid:
        await call.answer('В данном чате данный рейд не проходит')
        return
    if chatRaid.players[0].userId != call.from_user.id:
        await call.answer('Вы не лидер группы')
        return
    await endRecr(chatId=chatRaid.chatId)


async def endRecr(chatId: int):
    chatRaid = Raid.GetChatRaidByChat(chatId)
    scheduler.remove_job(f'raidRecr:{chatId}')
    if chatRaid:

        if len(chatRaid.players) > 1:
            text = f'<b>{chatRaid.boss.name}</b>:  ({chatRaid.boss.hp})   [0/{chatRaid.boss.ultaCharge}]\n'
            for player in chatRaid.players:
                st: FSMContext = dp.current_state(chat=player.chatId, user=player.userId)
                await st.set_state(RaidState.ready)
                await st.set_data(getFighterData(player))
                text += f'<b>{player.name}</b>:  ({player.hp})   [0/{UltaCharge}]\n'
                player.hp -= 15
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Драться яростно", callback_data=f"bossFightR:{chatRaid.id}"))
            keyboard.add(types.InlineKeyboardButton(text="Драться ловко", callback_data=f"bossFightD:{chatRaid.id}"))
            keyboard.add(types.InlineKeyboardButton(text="УЛЬТАНУТЬ", callback_data=f"bossUlta:{chatRaid.id}"))
            keyboard.add(types.InlineKeyboardButton(text="Защищаться", callback_data=f"bossDefence:{chatRaid.id}"))

            await bot.send_message(chat_id=chatId, text='НАЧИНАЕМ РЕЙД!')
            battleMessage = await bot.send_photo(chat_id=chatId,
                                                 photo=open(ROOT / 'static/bossFight/' / random.choice(
                                                     os.listdir(ROOT / 'static/bossFight')), 'rb'),
                                                 caption=text,
                                                 parse_mode='HTML',
                                                 reply_markup=keyboard
                                                 )
            actionMessage = await bot.send_message(chat_id=chatId, text='Действия бойцов:\n')
            chatRaid.AcceptRaid(actionMessage, battleMessage)

            extraSec = 0
            if len(chatRaid.players) > 5:
                extraSec = (len(chatRaid.players) - 5) * 3
            scheduler.add_job(outOfTime, trigger='interval', jobstore='local', args=[chatRaid.id],
                              seconds=35 + extraSec, id=f'boss_{chatRaid.id}')
        else:
            await bot.send_message(chat_id=chatId, text='Один в поле не войн, рейд не начат...')
            for player in chatRaid.players:
                st: FSMContext = dp.current_state(chat=player.chatId, user=player.userId)
                await st.set_state(None)
                Raid.EndRaidInChat(chatRaid)


async def InitAttackStep(chatRaidId: int, player: Player.Player, choice: str):
    chatRaid = Raid.GetChatRaid(chatRaidId)
    allAttack = True
    for player in chatRaid.players:
        st: FSMContext = dp.current_state(chat=chatRaid.chatId, user=player.userId)
        if (await st.get_state()) == 'RaidState:ready':
            allAttack = False
            break
    if allAttack:
        extraSec = 0
        if len(chatRaid.alives) > 5:
            extraSec = (len(chatRaid.alives) - 5) * 3
        scheduler.reschedule_job(job_id=f'boss_{chatRaid.id}', trigger='interval', seconds=35 + extraSec,
                                 jobstore='local')
        dead = False
        alives = 0
        text = ''
        target = chatRaid.bossTarget()
        bossUlta = 0
        if not target:
            text += '  Замахивается и пытается нанести урон каждому бойцу!\n'
        else:
            bossUlta = chatRaid.boosUlta()
            if bossUlta:
                text += f'  Прицеливается и пытается УЛЬТАНУТЬ в <i>{target.name}</i>!\n'
            else:
                text += f'  Прицеливается и пытается нанести урон в <i>{target.name}</i>!\n'

        if not bossUlta:
            chatRaid.boss.ulta += 1

        for player in chatRaid.players:
            playerText = ''
            st: FSMContext = dp.current_state(chat=chatRaid.chatId, user=player.userId)
            std = await st.get_data()
            stt = await st.get_state()
            if stt == 'RaidState:dead':
                text += f'\n<b>{player.name}</b> <i>Погиб...</i>'
                continue
            if stt == 'RaidState:runOut':
                text += f'\n<b>{player.name}</b> долго думал и босс задавил его...\n  <i>Погиб...</i>'
                await st.set_state(RaidState.dead)
                chatRaid.alives.remove(player)
                continue

            playerLuck = 1 if random.random() // (
                    std.get('luck') + (std.get('luck') * 0.55 * std.get('dexFactor'))) > 0 else 0
            bossLuck = 1 if (random.random() // chatRaid.boss.luck) > 0 else 0
            playerDamage = (std.get('damage') +
                            (std.get('damage') * 0.2 * std.get('rageFactor')) +
                            (std.get('damage') * std.get('ulta')))

            if not target or player.userId == target.userId:
                bossDamage = (chatRaid.boss.damage
                              - 0.3 * chatRaid.boss.damage * (1 if not target else 0)
                              + chatRaid.boss.damage * bossUlta
                              )

                if not std['defence']:
                    playerText += f'  Защищается от урона '
                elif not playerLuck:
                    playerText += f'  Уворачивается от урона '
                else:
                    await st.update_data(health=(std.get('health') - playerLuck * std['defence'] * bossDamage))
                    std = await st.get_data()
                    playerText += f'  Получает урон: {bossDamage} '
            else:
                playerText += f'  Не получает урона '

            if not bossLuck or not std['defence']:
                playerText += f'и не наносит урона'
            else:
                chatRaid.boss.hp -= playerDamage
                chatRaid.damagePie[player.userId] += playerDamage
                if std['ulta']:
                    playerText += f'и ультует: {round(playerDamage)}'
                else:
                    playerText += f'и наносит урон: {round(playerDamage)}'

            if std["health"] <= 0:
                playerText += f'\n  <i>Погиб...</i>'
                dead = True
                await st.set_state(RaidState.dead)
                chatRaid.alives.remove(player)
            else:
                alives += 1
                await st.set_state(RaidState.ready)

            await st.update_data(charge=std['charge'] + 1)

            text += f'\n<b>{player.name}</b>:  ({round(std["health"])})   [{std["charge"] + 1}/{UltaCharge}]\n' + playerText
        text = f'<b>{chatRaid.boss.name}</b>:  ({round(chatRaid.boss.hp)})   [{chatRaid.boss.ulta}/{chatRaid.boss.ultaCharge}]\n' + text + '\n'

        photoCategory = 'memberDead' if dead else 'bossFight'
        keyboard = chatRaid.battleMessage.reply_markup
        actionText = 'Действия бойцов:\n'
        if not alives:
            text += '\n<i>Все погибли...Пусть коллектор упокоит их тела.</i>'
            keyboard = None
            for player in chatRaid.players:
                st: FSMContext = dp.current_state(chat=chatRaid.chatId, user=player.userId)
                await st.set_state(None)
            scheduler.remove_job(f'boss_{chatRaid.id}', jobstore='local')
            Raid.EndRaidInChat(chatRaid)
        if chatRaid.boss.hp <= 0:
            keyboard = None
            photoCategory = 'bossWin'
            scheduler.remove_job(f'boss_{chatRaid.id}', jobstore='local')
            text += f'\n<b>БОСС ПАЛ!</b> Хвала инженерам!\n<b>Добыча:</b>\nОпыт: {chatRaid.boss.expReward}\nДеньги: {chatRaid.boss.moneyReward}'
            rewardText = 'Делим добычу, бойцы:\n'
            allDamage = sum((chatRaid.damagePie.values()))
            for player in chatRaid.players:
                st: FSMContext = dp.current_state(chat=chatRaid.chatId, user=player.userId)
                await st.set_state(None)
                rewardPart = chatRaid.damagePie[player.userId] / allDamage
                moneyPart = round(chatRaid.boss.moneyReward * rewardPart)
                expPart = round(chatRaid.boss.expReward * rewardPart)
                player.exp += expPart
                player.money += moneyPart
                await AchievementHandler.AddHistory(chatId=player.chatId, userId=player.userId, totalWinBoss=1,
                                                    totalMoney=moneyPart, totalExp=expPart)
                rewardText += f'\n<b>{player.name}</b>\n   Опыт: {expPart}   Деньги: {moneyPart}'
            item = Good.GetItem(chatRaid.boss.itemId)
            player = random.choice(chatRaid.alives)
            player.AddItem(item)
            rewardText += f'\n<b>{player.name}</b> забирает победный предмет: <i>{item.name}</i>!'
            Raid.EndRaidInChat(chatRaid)
            actionText = rewardText

        media = types.input_media.InputMediaPhoto(media=types.InputFile(
            ROOT / f'static/{photoCategory}/' / random.choice(os.listdir(ROOT / f'static/{photoCategory}'))),
            caption=text,
            parse_mode='HTML')
        await chatRaid.battleMessage.edit_media(media=media, reply_markup=keyboard)
        await chatRaid.actionMessage.edit_text(
            text=actionText,
            parse_mode='HTML'
        )
    else:
        text = chatRaid.actionMessage.text
        text += f'\n<b>{player.name}</b>\t{choice}\n'
        await chatRaid.actionMessage.edit_text(
            text=text,
            parse_mode='HTML'
        )


async def RageAttack(call: types.CallbackQuery, state: FSMContext):
    chatRaidId = call.data.replace("bossFightR:", '')

    player = Player.GetPlayer(call.message.chat.id, call.from_user.id)
    if not player:
        await call.answer('Нужно зарегистрироваться для такого')
        return

    chatRaid = Raid.GetChatRaid(chatRaidId)
    if not chatRaid:
        await call.answer("Это битва уже только в воспоминаниях...")
        return

    if not Raid.GetPlayer(player.chatId, player.userId):
        await call.answer('Вы не состоите в рейде')
        return

    await state.set_state(RaidState.attack)
    await state.update_data(rageFactor=1, dexFactor=0, defence=1, ulta=0)
    await InitAttackStep(chatRaidId, player, 'яростно атакует')
    await call.answer('Вы сделали свой выбор')


async def DexAttack(call: types.CallbackQuery, state: FSMContext):
    chatRaidId = call.data.replace("bossFightD:", '')

    player = Player.GetPlayer(call.message.chat.id, call.from_user.id)
    if not player:
        await call.answer('Нужно зарегистрироваться для такого')
        return

    chatRaid = Raid.GetChatRaid(chatRaidId)
    if not chatRaid:
        await call.answer("Это битва уже только в воспоминаниях...")
        return

    if not Raid.GetPlayer(player.chatId, player.userId):
        await call.answer('Вы не состоите в рейде')
        return

    await state.set_state(RaidState.attack)
    await state.update_data(rageFactor=0, dexFactor=1, defence=1, ulta=0)
    await InitAttackStep(chatRaidId, player, 'ловко атакует')
    await call.answer('Вы сделали свой выбор')


async def Ulta(call: types.CallbackQuery, state: FSMContext):
    chatRaidId = call.data.replace("bossUlta:", '')

    player = Player.GetPlayer(call.message.chat.id, call.from_user.id)
    if not player:
        await call.answer('Нужно зарегистрироваться для такого')
        return

    chatRaid = Raid.GetChatRaid(chatRaidId)
    if not chatRaid:
        await call.answer("Это битва уже только в воспоминаниях...")
        return

    if not Raid.GetPlayer(player.chatId, player.userId):
        await call.answer('Вы не состоите в рейде')
        return

    std = await state.get_data()
    if std.get('charge') < UltaCharge:
        await call.answer('Ультовать еще нельзя')
        return

    await state.update_data(charge=-1)
    await state.set_state(RaidState.attack)
    await state.update_data(rageFactor=0, dexFactor=0, defence=1, ulta=1)
    await InitAttackStep(chatRaidId, player, 'ультует!')
    await call.answer('Вы сделали свой выбор')


async def Defence(call: types.CallbackQuery, state: FSMContext):
    chatRaidId = call.data.replace("bossDefence:", '')

    player = Player.GetPlayer(call.message.chat.id, call.from_user.id)
    if not player:
        await call.answer('Нужно зарегистрироваться для такого')
        return

    chatRaid = Raid.GetChatRaid(chatRaidId)
    if not chatRaid:
        await call.answer("Это битва уже только в воспоминаниях...")
        return

    if not Raid.GetPlayer(player.chatId, player.userId):
        await call.answer('Вы не состоите в рейде')
        return

    await state.set_state(RaidState.attack)
    await state.update_data(rageFactor=0, dexFactor=0, defence=0, ulta=0)
    await InitAttackStep(chatRaidId, player, 'защищается')
    await call.answer('Вы сделали свой выбор')


async def outOfTime(chatRaidId: int):
    chatRaid = Raid.GetChatRaid(chatRaidId)
    for player in chatRaid.players:
        st: FSMContext = dp.current_state(chat=chatRaid.chatId, user=player.userId)
        stt = await st.get_state()
        if stt == 'RaidState:ready':
            await st.set_state(RaidState.runOut)
    await InitAttackStep(chatRaidId, None, None)


def register_handlers_raid(dp: Dispatcher):
    dp.register_message_handler(getRaidsList, commands='raid', state=None)
    dp.register_callback_query_handler(pageRaidsList, state=None, regexp='^bossList:*')
    dp.register_callback_query_handler(startRecr, state=None, regexp='^startRecr:*')
    dp.register_callback_query_handler(enterToRaid, state=[None, RaidState.awaiting], regexp='^enterRaid:*')
    dp.register_message_handler(leaveRaid, state=RaidState.awaiting, commands='raid_leave')
    dp.register_callback_query_handler(instantEndRecr, state=RaidState.awaiting, regexp='^endRecr:')

    dp.register_callback_query_handler(RageAttack, state=RaidState.ready, regexp='^bossFightR:*')
    dp.register_callback_query_handler(DexAttack, state=RaidState.ready, regexp='^bossFightD:*')
    dp.register_callback_query_handler(Defence, state=RaidState.ready, regexp='^bossDefence:*')
    dp.register_callback_query_handler(Ulta, state=RaidState.ready, regexp='^bossUlta:*')
