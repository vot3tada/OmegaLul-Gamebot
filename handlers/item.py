from aiogram.dispatcher import Dispatcher
from aiogram import types
import Classes.Player as Player
import Classes.Good as Good
import handlers.achievement as AchievementHandler

async def useItem(call : types.CallbackQuery):
    if not Player.FindPlayer(call.message.chat.id, call.from_user.id):
        await call.answer('Нужно зарегаться для такого')
        return
    player = Player.GetPlayer(call.message.chat.id, call.from_user.id)
    itemId: str = call.data.replace("item:",'')
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