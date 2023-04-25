import Classes.Achievement as Achiv
from typing import Any, Union
import requests
from pathlib import Path
import configparser

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

config = configparser.ConfigParser()
config.read(ROOT /'config.ini')
backhost = config['DEFAULT']['BACKHOST']
backport = config['DEFAULT']['BACKPORT']

class History():

    def __init__(self, chatId, userId, totalMoney = 0, totalExp = 0, totalQuestions = 0, totalFights = 0, totalWinFights = 0, totalWinBoss = 0,
                       totalItem = 0, totalTakenTasks = 0, totalEndedTasks = 0, totalFallTasks = 0, totalWinCollector = 0,
                         totalCreateEvent = 0, totalEnterEvent = 0, totalKickEvent = 0, totalLeaveFights = 0, totalCommits = 0, totalMerges = 0):
        self.chatId = chatId
        self.userId = userId
        self.totalMoney = totalMoney
        self.totalExp = totalExp
        self.totalQuestions = totalQuestions
        self.totalFights = totalFights
        self.totalWinFights = totalWinFights
        self.totalWinBoss = totalWinBoss
        self.totalItem = totalItem
        self.totalTakenTasks = totalTakenTasks
        self.totalEndedTasks = totalEndedTasks
        self.totalFallTasks = totalFallTasks
        self.totalWinCollector = totalWinCollector
        self.totalCreateEvent = totalCreateEvent
        self.totalEnterEvent = totalEnterEvent
        self.totalKickEvent = totalKickEvent
        self.totalLeaveFights = totalLeaveFights
        self.totalCommits = totalCommits
        self.totalMerges = totalMerges

    def to_json(self) -> dict[str, Any]:
        json = {
            "chatId": self.chatId,
            "userId": self.userId,
            "totalMoney": self.totalMoney,
            "totalExp": self.totalExp,
            "totalQuestions": self.totalQuestions,
            "totalFights": self.totalFights,
            "totalWinFights": self.totalWinFights,
            "totalWinBoss": self.totalWinBoss,
            "totalItem": self.totalItem,
            "totalTakenTasks": self.totalTakenTasks,
            "totalEndedTasks": self.totalEndedTasks,
            "totalFallTasks": self.totalFallTasks,
            "totalWinCollector": self.totalWinCollector,
            "totalCreateEvent": self.totalCreateEvent,
            "totalEnterEvent": self.totalEnterEvent,
            "totalKickEvent": self.totalKickEvent,
            "totalLeaveFights": self.totalLeaveFights,
            "totalCommits": self.totalCommits,
            "totalMerges": self.totalMerges
        }
        return json

    def UpdateHistory(self, totalMoney = 0, totalExp = 0, totalQuestions = 0, totalFights = 0, totalWinFights = 0, totalWinBoss = 0,
                       totalItem = 0, totalTakenTasks = 0, totalEndedTasks = 0, totalFallTasks = 0, totalWinCollector = 0,
                         totalCreateEvent = 0, totalEnterEvent = 0, totalKickEvent = 0, totalLeaveFights = 0, totalCommits = 0, totalMerges = 0):
        checkAchId = []
        def Updater(i: str, total: int):
            if (Achiv.Check(i, total) and i not in [j.id for j in Achiv.GetUserAchivs(self.chatId, self.userId)]):
                u = Achiv.UserAchievement(i, self.chatId, self.userId)
                Achiv.AddUserAchiv(u)
                checkAchId.append(i)

        updates = [ 
            (totalMoney, 'totalMoney'), 
            (totalExp, 'totalExp'), 
            (totalQuestions, 'totalQuestions'),
            (totalFights, 'totalFights'), 
            (totalWinFights, 'totalWinFights'), 
            (totalWinBoss, 'totalWinBoss'),
            (totalItem, 'totalItem'), 
            (totalTakenTasks, 'totalTakenTasks'), 
            (totalEndedTasks, 'totalEndedTasks'),
            (totalFallTasks, 'totalFallTasks'), 
            (totalWinCollector, 'totalWinCollector'),
            (totalCreateEvent, 'totalCreateEvent'), 
            (totalEnterEvent, 'totalEnterEvent'),
            (totalKickEvent, 'totalKickEvent'), 
            (totalLeaveFights, 'totalLeaveFights'),
            (totalCommits,'totalCommits'),
            (totalMerges,'totalMerges')
            ]

        for i, (value, attribute) in enumerate(updates):
            if value:
                setattr(self, attribute, getattr(self, attribute) + value)
                Updater(attribute, getattr(self, attribute))
        responce:requests.Response = requests.put(
                url=f'http://{backhost}:{backport}/api/history/update',
                json = self.to_json(),
                headers={"Content-Type": "application/json"})
        return checkAchId

def GetHistory(chatId: int, userId: int) -> Union[History, None]:
    responce:requests.Response = requests.get(
        url=f'http://{backhost}:{backport}/api/history/id/{chatId}/{userId}',
        headers={"Content-Type": "application/json"})
    
    if responce.status_code >= 400:
        return None
    
    history: History = History(**responce.json())
    return history