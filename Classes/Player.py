from Classes.Good import Good
from typing import Union

class Player():

    def __init__(self, 
                 chatId : int,
                 userId : int,
                 name: str, 
                 photo : str,
                 exp : int  = 0,
                 money: int  = 1000,
                 inventory : list[list[Good,int]] = [],
                 luck : float = 0.2,
                 luckMultiply : int = 1,
                 hp : int = 100,
                 damage : int = 20,
                 damageMultyply : int = 1,
                 status : list[Good] = []):
        self._chatId = chatId
        self._userId = userId
        self._name = name
        self._exp = exp
        self._money = money
        self._photo = photo
        self._inventory = inventory
        self._luck = luck
        self._luckMultiply = luckMultiply
        self._hp = hp
        self._damage = damage
        self._damageMultiply = damageMultyply
        self._status = status

    @property
    def chatId(self):
        return self._chatId

    @property
    def userId(self):
        return self._userId

    @property
    def name(self):
        return self._name

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, x :int):
        if x < 0:
            self._hp = 0
        elif x > 100:
            self._hp = 100
        else:
            self._hp = x

    @property
    def exp(self):
        return self._exp
    
    @exp.setter
    def exp(self, x: int):
        if self._exp >= x:
            raise ValueError('Опыт не может не увеличиваться')
        self._exp = x

    @property
    def money(self):
        return self._money
    
    @money.setter
    def money(self, x: int):
        if x < 0:
            raise ValueError('Баланс ушел в минус')
        self._money = x

    @property
    def level(self):
        _level = 0
        exp = self.exp
        while exp - 100 + 10 * _level >= 0:
            _level += 1 
            exp -= 100 + 10 * _level
        return _level
    
    @property
    def damage(self):
        return self._damage
    
    @property
    def damageMultiply(self):
        return self._damageMultiply
    
    @damageMultiply.setter
    def damageMultiply(self, x :int):
        if x < 0:
            raise ValueError('Множитель не может быть отрицательным')
        self._damageMultiply = x

    @property 
    def luck(self):
        return self._luck
        
    @property
    def luckMultiply(self):
        return self._luckMultiply
    
    @luckMultiply.setter
    def luckMultiply(self, x: int):
        if x < 0:
            raise ValueError('Множитель не может быть отрицательным')
        self._luckMultiply = x

    @property 
    def photo(self):
        return self._photo
    
    @property
    def inventory(self):
        return self._inventory.copy()
    
    @property
    def status(self):
        return self._status.copy()
    
    def FindItem(self, item : Good) -> bool:
        return item.id in [good[0].id for good in self._inventory]
    
    def GetItem(self, item : Good) -> Union[list[Good,int], None]:
        for _item in self._inventory:
            if _item[0].id == item.id:
                return _item
        return None 
    
    def AddItem(self, item : Good):
        if self.FindItem(item):
            self.GetItem(item)[1] += 1
        else:
            self._inventory.append([item, 1])
    
    def RemoveItem(self, item: Good):
        if not self.FindItem(item):
            raise ValueError('Попытка удалить несуществующий статус')
        _item : list[Good, int] = self.GetItem(item)
        _item[1] -= 1
        if not _item[1]:
            self._inventory.remove(_item)
    
    def FindStatus(self, item : Good) -> bool:
        return item.id in [good.id for good in self._status]
    
    def AddStatus(self, item : Good):
        if self.FindStatus(item):
            raise ValueError('Двойной статус запрещен')
        self._status.append(item)

    def GetStatus(self, item : Good) -> Union[Good, None]:
        for _item in self._status:
            if _item.id == item.id:
                return _item
        return None 

    def RemoveStatus(self, item : Good):
        if not self.FindStatus(item):
            raise ValueError('Попытка удалить несуществующий статус')
        self._status.remove(self.GetStatus(item))

Players :list[Player] = None

def GetAllPlayers():
    return Players.copy()

def FindPlayer(chat_id: int, user_id: int) -> bool:
    for player in Players:
        if player._userId == user_id and player._chatId == chat_id:
            return True
    return False

def GetPlayer(chat_id: int, user_id: int) -> Union[Player, None]:
    for player in Players:
        if player._userId == user_id and player._chatId == chat_id:
            return player
    return None 

def AddPlayer(player : Player):
    Players.append(player)