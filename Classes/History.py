import Classes.Achievement as Achiv


class History():

    def __init__(self):
        self.userChatId = 0
        self.userId = 0
        self._totalMoney = 0
        self._totalExp = 0
        self._totalQuestions = 0
        self._totalFights = 0
        self._totalWinFights = 0
        self._totalWinBoss = 0
        self._totalItem = 0
        self._totalTakenTasks = 0
        self._totalEndedTasks = 0
        self._totalFallTasks = 0
        self._totalWinCollector = 0
        self._totalCreateEvent = 0
        self._totalEnterEvent = 0
        self._totalKickEvent = 0
        self._totalLeaveFights = 0

    def UpdateHistory(self, totalMoney = 0, totalExp = 0, totalQuestions = 0, totalFights = 0, totalWinFights = 0, totalWinBoss = 0,
                       totalItem = 0, totalTakenTasks = 0, totalEndedTasks = 0, totalFallTasks = 0, totalWinCollector = 0,
                         totalCreateEvent = 0, totalEnterEvent = 0, totalKickEvent = 0, totalLeaveFights = 0):
        checkAchId = []
        def Updater(i: int, total: int):
            if (Achiv.Check(i, total) and i not in [j.achId for j in Achiv.GetUserAchivs(self.userChatId, self.userId)]):
                u = Achiv.UserAchievement()
                u.achId = i
                u.chatId = self.userChatId
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

        return checkAchId

his1 = History()
his1.userChatId = -884518885 
his1.userId = 1121151192
history: list[History] = [his1]

def GetHistory(chatId: int, userId: int):
    h = [i for i in history if i.userChatId == chatId and i.userId == userId]
    return h[0] if len(h) > 0 else None
        

    
        
    

        