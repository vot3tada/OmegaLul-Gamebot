from typing import Union
from Classes.Player import Player, GetPlayer
import copy
import datetime
from dateutil import tz
import random
from aiogram.types import Message

class Boss:

    def __init__(self,
                id: int,
                name: str,
                photo: str,
                hp: int,
                damage: int,
                luck: int,
                moneyReward: int,
                expReward: int,
                ultaCharge: int,
                cleaveRate: float
                 ) -> None:
        self.id = id
        self.name = name
        self.photo = photo
        self.hp = hp
        self.damage = damage
        self.luck = luck
        self.moneyReward = moneyReward
        self.expReward = expReward
        self.ultaCharge = ultaCharge
        self.cleaveRate = cleaveRate
        self.ulta = 0

Bosses: list[Boss] = [
    Boss(
        0,
        'Батя Коллектора',
        './static/boss/father.jpg',
        750,
        30,
        0.3,
        450,
        600,
        5,
        0.5
    ),
    Boss(
        1,
        'Жаба',
        './static/boss/frog.jpg',
        2000,
        15,
        0.1,
        700,
        800,
        8,
        0.3
    )
]

def GetBosses() -> list[Boss]:
    return Bosses.copy()

def GetBoss(bossId: int) -> Boss:
    for boss in Bosses:
        if boss.id == bossId:
            return copy.copy(boss)
    return None

class ChatRaid:

    def __init__(self, chatId: int, bossId: int, owner: Player) -> None:
        self.chatId: int = chatId
        self.boss: Boss = GetBoss(bossId)
        self.players: list[Player] = [owner]
        self.id = (datetime.datetime.now(tz.gettz("Europe/Moscow")).__str__()) + str(chatId) + str(bossId)
        self.actionMessage: Message = None
        self.battleMessage: Message = None

    def EnterToRaid(self, player: Player):
        self.players.append(player)
    
    def LeaveFromRaid(self, player: Player) -> bool:
        for _player in self.players:
            if _player.chatId == player.chatId and _player.userId == player.userId:
                self.players.remove(_player)
                return len(self.players)
    
    def GetPlayer(self, player: Player):
        for _player in self.players:
            if _player.chatId == player.chatId and _player.userId == player.userId:
                return player
        return None
    
    def bossTarget(self) -> Union[Player,None]:
        if random.random() <= self.boss.cleaveRate:
            return None
        else:
            return random.choice(self.players)

ChatRaids: list[ChatRaid] = []

def StartRaidInChat(chatId: int, bossId: int, userId: int) -> ChatRaid:
    chatRaid = ChatRaid(chatId, bossId, GetPlayer(chatId, userId))
    ChatRaids.append(chatRaid)
    return chatRaid

def EndRaidInChat(chatRaid: ChatRaid):
    ChatRaids.remove(chatRaid)

def GetChatRaid(chatRaidId: int) -> Union[ChatRaid,None]:
    for chatRaid in ChatRaids:
        if chatRaid.id == chatRaidId:
            return chatRaid
    return None
            
def GetChatRaidByChat(chatId: int) -> Union[ChatRaid,None]:
    for chatRaid in ChatRaids:
        if chatRaid.chatId == chatId:
            return chatRaid
    return None