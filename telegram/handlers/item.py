from aiogram.dispatcher import Dispatcher
from aiogram import types
import Classes.Player as Player
import Classes.Good as Good
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]


async def useItem(call : types.CallbackQuery):
    itemId, userId = call.data.replace("item:",'').split('_')
    itemId, userId = int(itemId), int(userId)
    if call.from_user.id != userId:
        await call.answer('Это не ваш инвентарь')
        return
    player = Player.GetPlayer(call.message.chat.id, call.from_user.id)
    good : Good.Good  = Good.GetItem(itemId)
    if not player.FindItem(good):
        await call.answer('Нет такого предмета')
        return
    if player.FindStatus(good):
        await call.answer('Предмет уже использован')
        return
    player.BuffByItem(good)
    player.RemoveItem(good)
    await call.answer('Предмет использован')
    keyboard = types.InlineKeyboardMarkup()
    for i in player.inventory:
        keyboard.add(types.InlineKeyboardButton(text = f'{i[0].name}: {i[1]}', callback_data=f"item:{i[0].id}"))
    await call.message.edit_reply_markup(keyboard)
    return

def register_handlers_item(dp: Dispatcher):
    dp.register_callback_query_handler(useItem, regexp='^item:*')