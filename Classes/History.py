import Classes.Achievement as Achiv
from typing import Any, Union
import requests

class History():

    def __init__(self, chatId, userId, totalMoney, totalExp, totalQuestions = 0, totalFights = 0, totalWinFights = 0, totalWinBoss = 0,
                       totalItem = 0, totalTakenTasks = 0, totalEndedTasks = 0, totalFallTasks = 0, totalWinCollector = 0,
                         totalCreateEvent = 0, totalEnterEvent = 0, totalKickEvent = 0, totalLeaveFights = 0):
        self.chatId = chatId
        self.userId = userId
        self._totalMoney = totalMoney
        self._totalExp = totalExp
        self._totalQuestions = totalQuestions
        self._totalFights = totalFights
        self._totalWinFights = totalWinFights
        self._totalWinBoss = totalWinBoss
        self._totalItem = totalItem
        self._totalTakenTasks = totalTakenTasks
        self._totalEndedTasks = totalEndedTasks
        self._totalFallTasks = totalFallTasks
        self._totalWinCollector = totalWinCollector
        self._totalCreateEvent = totalCreateEvent
        self._totalEnterEvent = totalEnterEvent
        self._totalKickEvent = totalKickEvent
        self._totalLeaveFights = totalLeaveFights

    def to_json(self) -> dict[str, Any]:
        json = {
            "chatId": self.chatId,
            "userId": self.userId,
            "totalMoney": self._totalMoney,
            "totalExp": self._totalExp,
            "totalQuestions": self._totalQuestions,
            "totalFights": self._totalFights,
            "totalWinFights": self._totalWinFights,
            "totalWinBoss": self._totalWinBoss,
            "totalItem": self._totalItem,
            "totalTakenTasks": self._totalTakenTasks,
            "totalEndedTasks": self._totalEndedTasks,
            "totalFallTasks": self._totalFallTasks,
            "totalWinCollector": self._totalWinCollector,
            "totalCreateEvent": self._totalCreateEvent,
            "totalEnterEvent": self._totalEnterEvent,
            "totalKickEvent": self._totalKickEvent,
            "totalLeaveFights": self._totalLeaveFights
        }
        return json

    def UpdateHistory(self, totalMoney = 0, totalExp = 0, totalQuestions = 0, totalFights = 0, totalWinFights = 0, totalWinBoss = 0,
                       totalItem = 0, totalTakenTasks = 0, totalEndedTasks = 0, totalFallTasks = 0, totalWinCollector = 0,
                         totalCreateEvent = 0, totalEnterEvent = 0, totalKickEvent = 0, totalLeaveFights = 0):
        checkAchId = []
        def Updater(i: int, total: int):
            if (Achiv.Check(i, total) and i not in [j.achId for j in Achiv.GetUserAchivs(self.chatId, self.userId)]):
                u = Achiv.UserAchievement()
                u.achId = i
                u.chatId = self.chatId
                u.userId = self.userId
                Achiv.AddUserAchiv(u)
                checkAchId.append(i)

        updates = [(totalMoney, '_totalMoney'), (totalExp, '_totalExp'), (totalQuestions, '_totalQuestions'),
                    (totalFights, '_totalFights'), (totalWinFights, '_totalWinFights'), (totalWinBoss, '_totalWinBoss'),
                      (totalItem, '_totalItem'), (totalTakenTasks, '_totalTakenTasks'), (totalEndedTasks, '_totalEndedTasks'),
                        (totalFallTasks, '_totalFallTasks'), (totalWinCollector, '_totalWinCollector'),
                          (totalCreateEvent, '_totalCreateEvent'), (totalEnterEvent, '_totalEnterEvent'),
                            (totalKickEvent, '_totalKickEvent'), (totalLeaveFights, '_totalLeaveFights')]

        for i, (value, attribute) in enumerate(updates):
            if value:
                setattr(self, attribute, getattr(self, attribute) + value)
                Updater(i, getattr(self, attribute))
            responce:requests.Response = requests.put(
                    url=f'http://localhost:8080/api/history/update',
                    json = self.to_json(),
                    headers={"Content-Type": "application/json"})
        return checkAchId

def GetHistory(chatId: int, userId: int) -> Union[History, None]:
    responce:requests.Response = requests.get(
        url=f'http://localhost:8080/api/history/id/{chatId}/{userId}',
        headers={"Content-Type": "application/json"})
    
    if responce.status_code >= 400:
        return None
    
    history: History = History(**responce.json())
    return history