from Classes.Good import Good
from typing import Union

class Player():

    userId : str 
    name : str
    exp : int
    money : int
    photo : str
    inventory : list[Good]

    luck : float
    luckMultiply : int

    hp : int
    damage : int
    damageMultiply : int

    status : list[Good]

    def __init__(self, 
                 userId : str,
                 name: str, 
                 photo : str,
                 exp : int  = 0,
                 money: int  = 1000,
                 inventory : list[Good] = [],
                 luck : float = 0.2,
                 luckMultiply : int = 1,
                 hp : int = 100,
                 damage : int = 20,
                 damageMultyply : int = 1,
                 status : list[Good] = []):
        self.userId = userId
        self.name = name
        self.exp = exp
        self.money = money
        self.photo = photo
        self.inventory = inventory
        self.luck = luck
        self.luckMultiply = luckMultiply
        self.hp = hp
        self.damage = damage
        self.damageMultiply = damageMultyply
        self.status = status

Players :list[Player] = None

def FindPlayer(id: str) -> bool:
    return id in [player.userId for player in Players]

def GetPlayer(id : str) -> Union[Player, None]:
    for player in Players:
        if player.userId == id:
            return player
    return None 


