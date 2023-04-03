import Classes.Player as Player
from Classes.Good import Good
from utils.scheduler import scheduler
    
class HPPotion(Good):

    name : str = 'Жигули Барное'
    id : str = 'HPPotion'
    price : int = 50
    description : str = 'Хиляет перса'

    def Effect(self, user_id_from : int, user_id_to : int = 0) -> bool:
        player = Player.GetPlayer(user_id_from)
        player.hp += 50
        return True


class LuckPotion(Good):

    name : str = 'Немного удачи'
    id : str = 'LuckPotion'
    price : int = 200
    description : str = 'Увеличивает удачу'

    def Effect(self, user_id_from : int, user_id_to : int = 0) -> bool:
        if not scheduler.get_job(f'{self.id}_{user_id_from}') is None:
            return False
        player = Player.GetPlayer(user_id_from)
        player.luckMultiply *= 1.5
        player.AddStatus(self)
        item_id = f'item_{self.id}_{user_id_from}'
        scheduler.add_job(self.endEffect, trigger='interval', seconds=10, args=[user_id_from, item_id], id=item_id)
        return True
    
    def endEffect(self, player_id : int, item_id : int):
        player = Player.GetPlayer(player_id)
        player.luckMultiply /= 1.5
        player.RemoveStatus(self)
        scheduler.remove_job(item_id)
    

class DamagePotion(Good):

    name : str = 'Немного дамага'
    id : str = 'DamagePotion'
    price : int = 200
    description : str = 'Увеличивает силу'

    def Effect(self, user_id_from : int, user_id_to : int = 0) -> bool:
        if not scheduler.get_job(f'{self.id}_{user_id_from}') is None:
            return False
        player = Player.GetPlayer(user_id_from)
        player.damageMultiply *= 1.5
        player.AddStatus(self)
        item_id = f'item_{self.id}_{user_id_from}'
        scheduler.add_job(self.endEffect, trigger='interval', seconds=10, args=[user_id_from, item_id], id=item_id)
        return True

    def endEffect(self ,player_id : int, item_id : int):
        player = Player.GetPlayer(player_id)
        player.damageMultiply /= 1.5
        player.RemoveStatus(self)
        scheduler.remove_job(item_id)
    

Items : dict[str, Good] = {
    HPPotion.id : HPPotion(),
    LuckPotion.id : LuckPotion(),
    DamagePotion.id : DamagePotion(),
}

def FindItem(id : str) -> bool:
    for item in Items.values():
        if item.id == id:
            return True
    return False

    
