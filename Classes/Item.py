import Classes.Player as Player
from Classes.Good import Good
from utils.scheduler import scheduler
    
class HPPotion(Good):

    name : str = 'Жигули Барное'
    id : str = 'HPPotion'
    price : int = 50
    description : str = 'Хиляет перса'

    @classmethod
    def Effect(cls, user_id_from : int, user_id_to : int = 0) -> bool:
        player = Player.GetPlayer(user_id_from)
        player.hp += 50
        if player.hp > 100: player.hp = 100
        return True


class LuckPotion(Good):

    name : str = 'Немного удачи'
    id : str = 'LuckPotion'
    price : int = 200
    description : str = 'Увеличивает удачу'

    @classmethod
    def Effect(cls, user_id_from : int, user_id_to : int = 0) -> bool:
        player = Player.GetPlayer(user_id_from)
        player.luckMultiply *= 1.5
        if not scheduler.get_job(f'{cls.id}_{user_id_from}') is None:
            return False
        player.status[f'{cls.id}_{user_id_from}'] = f'{cls.name}: 1.5х удачи'
        scheduler.add_job(cls.endEffect, trigger='interval', hours=2, args=[user_id_from], id=f'item_{cls.id}_{user_id_from}')
        return True
    
    @classmethod
    def endEffect(cls, player_id : int, item_id : str):
        player = Player.GetPlayer(player_id)
        player.luckMultiply /= 1.5
        player.status[f'item_{item_id}_{player_id}'] = None
        scheduler.remove_job(f'{item_id}_{player_id}')
    

class DamagePotion(Good):

    name : str = 'Немного дамага'
    id : str = 'DamagePotion'
    price : int = 200
    description : str = 'Увеличивает силу'

    @classmethod
    def Effect(cls, user_id_from : int, user_id_to : int = 0) -> bool:
        player = Player.GetPlayer(user_id_from)
        player.damageMultiply *= 1.5
        if not scheduler.get_job(f'{cls.id}_{user_id_from}') is None:
            return False
        player.status[f'{cls.id}_{user_id_from}'] = f'{cls.name}: 1.5х урона'
        scheduler.add_job(cls.endEffect, trigger='interval', hours=2, args=[user_id_from], id=f'item_{cls.id}_{user_id_from}')
        return True

    @classmethod
    def endEffect(cls ,player_id : int):
        player = Player.GetPlayer(player_id)
        player.damageMultiply /= 1.5
        player.status[f'item_{cls.id}_{player_id}'] = None
        scheduler.remove_job(f'{cls.id}_{player_id}')
    

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

    
