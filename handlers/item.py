from aiogram.dispatcher import Dispatcher
from aiogram import types
import Classes.Player as Player
import Classes.Item as Item

async def useItem(call : types.CallbackQuery):
    if not Player.FindPlayer(f'{call.message.chat.id}_{call.from_user.id}'):
        await call.answer('Нужно зарегаться для такого')
        return
    player = Player.GetPlayer(f'{call.message.chat.id}_{call.from_user.id}')
    itemId: str = call.data.replace("item:",'')
    good : Item.Item = Item.Items[itemId]
    if not player.FindItem(good):
        await call.answer('Нет такого предмета')
        return
    good.Effect(f'{call.message.chat.id}_{call.from_user.id}')
    player.RemoveItem(good)
    await call.answer('Предмет использован')
    return

def register_handlers_item(dp: Dispatcher):
    dp.register_callback_query_handler(useItem, regexp='^item:*')