import datetime
from dateutil import tz
import Classes.Player as Player

class Task():

    def __init__(self, name: str, chatId: int, userId: int, id: int, money: int, duration: int) -> None:
        self.id = id
        self.name = name
        self.chatId = chatId
        self.ownerUserId = userId
        self.money = money
        self.duration = duration
        self.workerUserId: int = -1
        self.deadline: datetime.datetime = None

Tasks: list[Task] = [
    Task( 'Водочка1', -884518885, 546270371, 0, 200, 93690),
    Task( 'Водочка2', -884518885, 546270371, 1, 200, 7200),
    Task( 'Водочка3', -884518885, 546270371, 2, 200, 7200),
    Task( 'Водочка4', -884518885, 546270371, 3, 200, 7200),
    Task( 'Водочка5', -884518885, 546270371, 4, 200, 7200),
    Task( 'Водочка6', -884518885, 546270371, 5, 200, 7200),
    Task( 'Водочка7', -884518885, 546270371, 6, 200, 7200),
    Task( 'Водочка8', -884518885, 546270371, 7, 200, 7200),
    Task( 'Водочка9', -884518885, 546270371, 8, 200, 60)
]

def FindTask(taskId: int) -> bool:
    return True if GetTask(taskId) else False

def GetAllTasks() -> list[Task]:
    return Tasks.copy()

def GetFreeTasks() -> list[Task]:
    tasks: list[Task] = []
    for task in Tasks:
        if task.workerUserId == -1:
            tasks.append(task)
    return tasks

def GetPlayerGivenTasks(chatId: int, userId: int) -> list[Task]:
    tasks: list[Task] = []
    for task in Tasks:
        if task.chatId == chatId and task.ownerUserId == userId:
            tasks.append(task)
    return tasks

def GetPlayerTakenTasks(chatId: int, userId: int) -> list[Task]:
    tasks: list[Task] = []
    for task in Tasks:
        if task.chatId == chatId and task.workerUserId == userId:
            tasks.append(task)
    return tasks

def GetTask(taskId: int) -> Task:
    for task in Tasks:
        if taskId == task.id:
            return task
    return None

def TakeTask(player: Player.Player, task: Task):
    task.workerUserId = player.userId
    task.deadline =  datetime.datetime.now(tz.gettz("Europe/Moscow")) + datetime.timedelta(seconds=task.duration)

def RefuseTask(player: Player.Player, task: Task) -> bool:
    task.workerUserId = -1
    punished = False
    date1 = (task.deadline - datetime.datetime.now(tz.gettz("Europe/Moscow")))
    if  date1 / datetime.timedelta(seconds=task.duration) < 0.7:
        punished = True 
    task.deadline = None
    return punished

def AddTask(task: Task):
    Tasks.append(task)

def DeleteTask(task: Task):
    for _task in Tasks:
        if _task.id == task.id:
            Tasks.remove(_task)
            return