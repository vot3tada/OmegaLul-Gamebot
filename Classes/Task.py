from datetime import datetime

class Task():

    def __init__(self, id: int, name: str, chatId: int, userId: int, deadline: datetime, money: int) -> None:
        self.id = id
        self.name = name
        self.chatId = chatId
        self.userId = userId
        self.deadline: datetime = deadline
        self.money = money

Tasks: list[Task] = []