from datetime import datetime

class Task():

    def __init__(self, name: str, chatId: int, userId: int, id: int,  deadline: datetime, money: int) -> None:
        self.id = id
        self.name = name
        self.chatId = chatId
        self.userId = userId
        self.deadline: datetime = deadline
        self.money = money

Tasks: list[Task] = []

def AddTask(task: Task):
    Tasks.append(task)