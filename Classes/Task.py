from datetime import datetime

class Task():

    def __init__(self, name: str, chatId: int, userId: int, id: int,  deadline: datetime, money: int) -> None:
        self.id = id
        self.name = name
        self.chatId = chatId
        self.userId = userId
        self.deadline: datetime = deadline
        self.money = money

Tasks: list[Task] = [
    Task( 'Водочка1', -884518885, 546270371, 0, datetime(2023,12,12), 200),
    Task( 'Водочка2', -884518885, 546270371, 1, datetime(2023,12,12), 200),
    Task( 'Водочка3', -884518885, 546270371, 2, datetime(2023,12,12), 200),
    Task( 'Водочка4', -884518885, 546270371, 3, datetime(2023,12,12), 200),
    Task( 'Водочка5', -884518885, 546270371, 4, datetime(2023,12,12), 200),
    Task( 'Водочка6', -884518885, 546270371, 5, datetime(2023,12,12), 200),
    Task( 'Водочка7', -884518885, 546270371, 6, datetime(2023,12,12), 200),
    Task( 'Водочка8', -884518885, 546270371, 7, datetime(2023,12,12), 200),
    Task( 'Водочка9', -884518885, 546270371, 8, datetime(2023,12,12), 200)
]

def GetAllTasks() -> list[Task]:
    return Tasks.copy()

def GetPlayerTasks(chatId: int, userId: int) -> list[Task]:
    tasks: list[Task] = []
    for task in Tasks:
        if task.chatId == chatId and task.userId == userId:
            tasks.append(task)
    return tasks

def GetTask(taskId: int) -> Task:
    for task in Tasks:
        if taskId == task.id:
            return task
    return None

def AddTask(task: Task):
    Tasks.append(task)