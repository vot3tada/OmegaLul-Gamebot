from aiogram.dispatcher import Dispatcher
from aiogram import types
import Classes.Player as Player
import Classes.Item as Item
from Classes.Good import Good

async def useItem(call : types.CallbackQuery):
    if not Player.FindPlayer(f'{call.message.chat.id}_{call.from_user.id}'):
        await call.answer('Нужно зарегаться для такого')
        return
    player = Player.GetPlayer(f'{call.message.chat.id}_{call.from_user.id}')
    itemId: str = call.data.replace("item:",'')
    good : Good = Item.Items[itemId]
    if not player.inventory.count(good):
        await call.answer('Нет такого предмета')
        return
    itemIndex = player.inventory.index(good)
    good.Effect(f'{call.message.chat.id}_{call.from_user.id}')
    player.inventory.pop(itemIndex)
    await call.answer('Предмет использован')
    return

def register_handlers_item(dp: Dispatcher):
    dp.register_callback_query_handler(useItem, regexp='^item:*')