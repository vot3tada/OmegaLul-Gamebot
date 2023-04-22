from typing import Union
from Classes.Player import Player, GetPlayer
import copy
import datetime
from dateutil import tz
import random
from aiogram.types import Message
from pathlib import Path
import configparser

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

config = configparser.ConfigParser()
config.read(ROOT /'config.ini')
backhost = config['DEFAULT']['BACKHOST']
backport = config['DEFAULT']['BACKPORT']


class Boss:

    def __init__(self,
                 id: int,
                 name: str,
                 photo: str,
                 hp: int,
                 damage: int,
                 luck: float,
                 moneyReward: int,
                 expReward: int,
                 ultaCharge: int,
                 cleaveRate: float,
                 ultaRate: float,
                 itemId: int
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
        self.ultaRate = ultaRate
        self.itemId = itemId

        self.ulta = 0


Bosses: list[Boss] = [
    Boss(
        id=0,
        name='Батя Коллектора',
        photo='father.jpg',
        hp=750,
        damage=47,
        luck=0.3,
        moneyReward=1000,
        expReward=850,
        ultaCharge=5,
        cleaveRate=0.35,
        ultaRate=0.5,
        itemId=33
    ),
    Boss(
        1,
        'Кыксик',
        'kiksik.jpg',
        690,
        49,
        0.65,
        1200,
        1050,
        2,
        0.51,
        0.1,
        34
    ),
    Boss(
        2,
        'Жаба',
        'frog.jpg',
        1200,
        30,
        0.1,
        1500,
        1300,
        6,
        0.7,
        0.9,
        35
    ),
    Boss(
        3,
        'Местный Каламит',
        'dragon.jpg',
        1500,
        46,
        0.45,
        2000,
        1800,
        7,
        0.51,
        0.4,
        36
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
        self.alives: list[Player] = None
        self.damagePie: dict[int, int] = {}

    def AcceptRaid(self, actionMessage: Message, battleMessage: Message):
        self.actionMessage = actionMessage
        self.battleMessage = battleMessage
        self.alives = self.players.copy()
        for player in self.players:
            self.damagePie[player.userId] = 0

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

    def bossTarget(self) -> Union[Player, None]:
        if random.random() <= self.boss.cleaveRate:
            return None
        return random.choice(self.alives)

    def boosUlta(self) -> int:
        if (self.boss.ulta >= self.boss.ultaCharge and
                random.random() > self.boss.ultaRate + (0.075 * (self.boss.ulta - self.boss.ultaCharge))):
            self.boss.ulta = 0
            return 1
        return 0


ChatRaids: list[ChatRaid] = []


def StartRaidInChat(chatId: int, bossId: int, userId: int) -> ChatRaid:
    chatRaid = ChatRaid(chatId, bossId, GetPlayer(chatId, userId))
    ChatRaids.append(chatRaid)
    return chatRaid


def EndRaidInChat(chatRaid: ChatRaid):
    ChatRaids.remove(chatRaid)


def GetChatRaid(chatRaidId: str) -> Union[ChatRaid, None]:
    for chatRaid in ChatRaids:
        if chatRaid.id == chatRaidId:
            return chatRaid
    return None


def GetChatRaidByChat(chatId: int) -> Union[ChatRaid, None]:
    for chatRaid in ChatRaids:
        if chatRaid.chatId == chatId:
            return chatRaid
    return None
