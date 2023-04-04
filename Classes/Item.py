import Classes.Player as Player
from Classes.Good import Good
from utils.scheduler import scheduler

class Item(Good):

    def buff(self, player: Player.Player):
        pass

    def debuff(self, player: Player.Player):
        pass

    def Effect(self, user_id_from : int, user_id_to : int = 0) -> bool:
        if not scheduler.get_job(f'{self.id}_{user_id_from}') is None:
            raise ValueError('Попытка применения двойного эффекта')
        player = Player.GetPlayer(user_id_from)
        self.buff(player)
        if self.duration:
            player.AddStatus(self)
            item_id = f'item_{self.id}_{user_id_from}'
            scheduler.add_job(self.endEffect, trigger='interval', seconds=self.duration, args=[user_id_from, item_id], id=item_id)
        return True
    
    def endEffect(self, player_id : int, item_id : int):
        player = Player.GetPlayer(player_id)
        self.debuff(player)
        player.RemoveStatus(self)
        scheduler.remove_job(item_id)

    
class HPPotion(Item):

    name : str = 'Жигули Барное'
    id : str = 'HPPotion'
    price : int = 50
    description : str = 'Хиляет перса'
    duration : int = 0

    def buff(self, player : Player.Player):
        player.hp += 50


class LuckPotion(Item):

    name : str = 'Немного удачи'
    id : str = 'LuckPotion'
    price : int = 200
    description : str = 'Увеличивает удачу'

    def buff(self, player : Player.Player):
        player.luckMultiply *= 1.5

    def debuff(self, player: Player.Player):
        player.luckMultiply /= 1.5
    

class DamagePotion(Item):

    name : str = 'Немного дамага'
    id : str = 'DamagePotion'
    price : int = 200
    description : str = 'Увеличивает силу'

    def buff(self, player : Player.Player):
        player.luckMultiply *= 1.5

    def debuff(self, player: Player.Player):
        player.luckMultiply /= 1.5
    

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

    
