import Classes.Good as Good
from typing import Any, Union
from utils.scheduler import scheduler
import apscheduler.job
import requests
import configparser
from pathlib import Path
import random

levelLuckFactor = 0.005
levelDamageFactor = 1

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

config = configparser.ConfigParser()
config.read(ROOT /'config.ini')
backhost = config['DEFAULT']['BACKHOST']
backport = config['DEFAULT']['BACKPORT']


class Player():
    def __init__(self, 
                 personPk: dict[str, int],
                 name: str, 
                 photo : str,
                 experience : int  = 0,
                 experienceMultiply: int = 1,
                 money: int  = 1000,
                 luck : float = 0.2,
                 luckMultiply : int = 1,
                 hp : int = 100,
                 damage : int = 20,
                 damageMultiply : int = 1,):
        self._chatId = personPk['chatId']
        self._userId = personPk['userId']
        self._name = name
        self._exp = experience
        self._experienceMultiply = experienceMultiply
        self._money = money
        self._photo = photo
        self._luck = luck
        self._luckMultiply = luckMultiply
        self._hp = hp
        self._damage = damage
        self._damageMultiply = damageMultiply

        responce: requests.Response = requests.get(
            url=f'http://{backhost}:{backport}/api/inventory/id/{self._chatId}/{self._userId}',
            headers={"Content-Type": "application/json"})
        data: list[dict[str, Any]] = responce.json()
        if responce.status_code == 404:
            self._inventory = []
        else:
            self._inventory: list[Good.Good, int] = [[Good.GetItem(good['itemId']), good['count']] for good in data]

        scheduler


    def to_json(self, withIds = True) -> dict[str, Any]:
        json = {
            'name': self._name,
            "experience": self._exp,
            "experienceMultiply": self._experienceMultiply,
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
    
    @name.setter
    def name(self, x: str):
        self._name = x
        self._updatePlayer()

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
        self._exp = x * self.expMultiply
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
    def fullLuck(self):
        return (self._luck + levelLuckFactor * self.level) * self._luckMultiply

    @property
    def expMultiply(self):
        return self._experienceMultiply
    
    @expMultiply.setter
    def expMultiply(self, x: int):
        if x < 0:
            raise ValueError('Множитель не может быть отрицательным')
        self._luckMultiply = x
        self._updatePlayer()

    @property 
    def photo(self):
        return self._photo
    
    @property
    def inventory(self) -> list[Good.Good, int]:
        return self._inventory.copy()
    
    def FindItem(self, item : Good.Good) -> bool:
        return item.id in [good[0].id for good in self._inventory]
    
    def GetItem(self, item : Good.Good) -> Union[list[Good.Good,int], None]:
        for _item in self._inventory:
            if _item[0].id == item.id:
                return _item
        return None 
    
    def AddItem(self, item : Good.Good):
        if self.FindItem(item):
             good = self.GetItem(item)
             good[1] += 1
        else:
            good = [item, 1]
            self._inventory.append(good)
        
        response: requests.Response = requests.put(
            url=f'http://{backhost}:{backport}/api/inventory/update',
            json = {
                "itemId":item.id,
                "count": good[1],
                "chatId": self._chatId,
                "userId": self._userId
            },
            headers={"Content-Type": "application/json"})
    
        if not response.ok:
            raise RuntimeError(f'Добавление предмета пользователю: {response.status_code}')
    
    def RemoveItem(self, item: Good):
        if not self.FindItem(item):
            raise ValueError('Попытка удалить несуществующий предмет')
        _item : list[Good.Good, int] = self.GetItem(item)
        _item[1] -= 1
        if not _item[1]:

            for __item in self._inventory:
                if __item[0].id == item.id:
                    self._inventory.remove(__item)
                    break
            
            response: requests.Response = requests.delete(
                url=f'http://{backhost}:{backport}/api/inventory/delete',
                json = {
                    "itemId":_item[0].id,
                    "chatId": self._chatId,
                    "userId": self._userId
                },
                headers={"Content-Type": "application/json"})
            if not response.ok:
                raise RuntimeError(f'Измененеие пользователя: {response.status_code}')
        else:
            response: requests.Response = requests.put(
                url=f'http://{backhost}:{backport}/api/inventory/update',
                json = {
                    "itemId":_item[0].id,
                    "count": _item[1],
                    "chatId": self._chatId,
                    "userId": self._userId
                },
                headers={"Content-Type": "application/json"})
            if response.status_code != 204:
                raise RuntimeError(f'Измененеие пользователя: {response.status_code}')

    def FindStatus(self,item: Good.Good) -> bool:
        return scheduler.get_job(f'buff:{item.id}_{self._chatId}_{self._userId}') != None

    def GetStatus(self) -> list[Good.Good]:
        goods:list[Good.Good] = [] 
        for job in scheduler.get_jobs():
            job: apscheduler.job.Job
            if str.find(job.id, 'buff') != -1:
                itemId, chatId, userId = str.replace(job.id,'buff:','').split('_')
                itemId, chatId, userId = int(itemId), int(chatId), int(userId)
                if userId == self._userId and chatId == self._chatId:
                    goods.append(Good.GetItem(itemId))
        return goods
        
    def BuffByItem(self, item: Good.Good):
        if not scheduler.get_job(f'buff:{item.id}_{self._chatId}_{self._userId}') is None:
            raise ValueError('Попытка применения двойного эффекта')
        
        for key in item.effects:
            setattr(self, key['property'], getattr(self, key['property']) + key['value'])

        if item.duration:
            buff_id = f'buff:{item.id}_{self._chatId}_{self._userId}'
            scheduler.add_job(_debuffByItem, trigger='interval', seconds=item.duration, args=[self.chatId, self.userId, item], id=buff_id)

    def _updatePlayer(self):

        response = requests.put(
            url=f'http://{backhost}:{backport}/api/person/update?userId={self._userId}&chatId={self._chatId}',
            headers={"Content-Type": "application/json"},
            json=self.to_json(False)
            )
        if response.status_code != 204:
            raise RuntimeError(f'Измененеие пользователя: {response.status_code}')

def _debuffByItem(chatId: int, userId: int, item: Good.Good):
    buff_id = f'buff:{item.id}_{chatId}_{userId}'
    scheduler.remove_job(buff_id)
    player = GetPlayer(chatId, userId)
    for key in item.effects:
        setattr(player, key['property'], getattr(player, key['property']) - key['value'])

def GetAllPlayers(chatId : int) -> list[Player]:

    responce:requests.Response = requests.get(
        url=f'http://{backhost}:{backport}/api/person/id/{chatId}',
        headers={"Content-Type": "application/json"})

    if responce.status_code == 404:
        return []
    
    data: list[dict[str, Any]] = responce.json()
    Players = [Player(**person) for person in data]

    return Players

def FindPlayer(chatId: int, userId: int) -> bool:

    responce:requests.Response = requests.get(
        url=f'http://{backhost}:{backport}/api/person/id/{chatId}',
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
        url=f'http://{backhost}:{backport}/api/person/id/{chatId}',
        headers={"Content-Type": "application/json"})

    if not responce.ok:
        raise RuntimeError(f'Поиск пользователя: {responce.status_code}')
    
    data: list[dict[str, Any]] = responce.json()
    Players = [Player(**person) for person in data]

    for player in Players:
        if player._userId == userId and player._chatId == chatId:
            return player
    return None 

def AddPlayer(player : Player):

    response: requests.Response = requests.post(
        url=f'http://{backhost}:{backport}/api/person/create',
        json = player.to_json(),
        headers={"Content-Type": "application/json"})
    
    if response.status_code != 201:
        raise RuntimeError(f'Добавление пользователя: {response.status_code}')

def GetRandomPlayer(chatId: int):
    players = GetAllPlayers(chatId)
    sumLuck = sum(i.fullLuck for i in players)
    index = random.randint(0, sumLuck)

    
