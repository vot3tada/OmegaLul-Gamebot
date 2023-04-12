from Classes.Good import Good
from typing import Any, Union
from utils.scheduler import scheduler
import requests
import json

class Player():
    def __init__(self, 
                 personPk: dict[str, int],
                 name: str, 
                 photo : str,
                 experience : int  = 0,
                 experienceMultiply: int = 1,
                 money: int  = 1000,
                 inventory : list[list[Good,int]] = [],
                 luck : float = 0.2,
                 luckMultiply : int = 1,
                 hp : int = 100,
                 damage : int = 20,
                 damageMultiply : int = 1,
                 status : list[Good] = []):
        self._chatId = personPk['chatId']
        self._userId = personPk['userId']
        self._name = name
        self._exp = experience
        self._experienceMultiply = experienceMultiply
        self._money = money
        self._photo = photo
        self._inventory = inventory
        self._luck = luck
        self._luckMultiply = luckMultiply
        self._hp = hp
        self._damage = damage
        self._damageMultiply = damageMultiply
        self._status = status

    def to_json(self, withIds = True) -> dict[str, Any]:
        json = {
            'name': self._name,
            "experience": self._exp,
            "experienceMultiply": 1,
            "money": self._money,
            "photo": self._photo,
            "luck": self._luck,
            "luckMultiply": self._luckMultiply,
            "hp": self._hp,
            "damage": self._damage,
            "damageMultiply": self._damageMultiply,
            
        }
        if withIds:
            json['personPk'] = {
                "chatId": self.chatId,
                "userId": self.userId
            }
        return json


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
        self._updatePlayer()
    

    @property
    def exp(self):
        return self._exp
    
    @exp.setter
    def exp(self, x: int):
        if self._exp >= x:
            raise ValueError('Опыт не может не увеличиваться')
        self._exp = x
        self._updatePlayer()

    @property
    def money(self):
        return self._money
    
    @money.setter
    def money(self, x: int):
        if x < 0:
            raise ValueError('Баланс ушел в минус')
        self._money = x
        self._updatePlayer()

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
        self._updatePlayer()

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
        self._updatePlayer()

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
        self._updatePlayer()
    
    def RemoveItem(self, item: Good):
        if not self.FindItem(item):
            raise ValueError('Попытка удалить несуществующий статус')
        _item : list[Good, int] = self.GetItem(item)
        _item[1] -= 1
        if not _item[1]:
            self._inventory.remove(_item)
        self._updatePlayer()
    
    def FindStatus(self, item : Good) -> bool:
        return item.id in [good.id for good in self._status]
    
    def AddStatus(self, item : Good):
        if self.FindStatus(item):
            raise ValueError('Двойной статус запрещен')
        self._status.append(item)
        self._updatePlayer()

    def GetStatus(self, item : Good) -> Union[Good, None]:
        for _item in self._status:
            if _item.id == item.id:
                return _item
        return None 

    def RemoveStatus(self, item : Good):
        if not self.FindStatus(item):
            raise ValueError('Попытка удалить несуществующий статус')
        status = self.GetStatus(item)
        self._status.remove(status)
        self._updatePlayer()

    def BuffByItem(self, item: Good):
        if not scheduler.get_job(f'{item.id}_{self._chatId}_{self._userId}') is None:
            raise ValueError('Попытка применения двойного эффекта')
        
        for key in item.effects.keys():
            setattr(self, key, getattr(self, key) + item.effects[key])

        if item.duration:
            self.AddStatus(item)
            buff_id = f'{item.id}_{self._chatId}_{self._userId}'
            scheduler.add_job(_debuffByItem, trigger='interval', seconds=item.duration, args=[self.chatId, self.userId, item], id=buff_id)

    def _updatePlayer(self):

        response = requests.put(
            url=f'http://localhost:8080/api/person/update?userId={self._userId}&chatId={self._chatId}',
            headers={"Content-Type": "application/json"},
            json=self.to_json(False)
            )
        if response.status_code != 204:
            raise RuntimeError(f'Измененеие пользователя: {response.status_code}')

def _debuffByItem(chatId: int, userId: int, item: Good):
    player = GetPlayer(chatId, userId)
    buff_id = f'{item.id}_{chatId}_{userId}'
    for key in item.effects.keys():
        setattr(player, key, getattr(player, key) - item.effects[key])
    player.RemoveStatus(item)
    scheduler.remove_job(buff_id)

def GetAllPlayers(chatId : int) -> list[Player]:

    responce:requests.Response = requests.get(
        url=f'http://localhost:8080/api/person/id/{chatId}',
        headers={"Content-Type": "application/json"})

    if responce.status_code == 404:
        return False
    
    data: list[dict[str, Any]] = responce.json()
    Players = [Player(**person) for person in data]

    return Players

def FindPlayer(chatId: int, userId: int) -> bool:

    responce:requests.Response = requests.get(
        url=f'http://localhost:8080/api/person/id/{chatId}',
        headers={"Content-Type": "application/json"})

    if responce.status_code == 404:
        return False
    
    data: list[dict[str, Any]] = responce.json()
    Players = [Player(**person) for person in data]

    for player in Players:
        if player._userId == userId:
            return True
    return False

def GetPlayer(chatId: int, userId: int) -> Union[Player, None]:

    responce:requests.Response = requests.get(
        url=f'http://localhost:8080/api/person/id/{chatId}',
        headers={"Content-Type": "application/json"})

    if responce.status_code == 404:
        return False
    
    data: list[dict[str, Any]] = responce.json()
    Players = [Player(**person) for person in data]

    for player in Players:
        if player._userId == userId and player._chatId == chatId:
            return player
    return None 

def AddPlayer(player : Player):

    response: requests.Response = requests.post(
        url=f'http://localhost:8080/api/person/create',
        json = player.to_json(),
        headers={"Content-Type": "application/json"})
    
    if response.status_code != 201:
        raise RuntimeError(f'Добавление пользователя: {response.status_code}')

    
