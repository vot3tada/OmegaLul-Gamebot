import datetime
from typing import Any
from dateutil import tz
import Classes.Player as Player
from utils.scheduler import scheduler
import requests

class Task():

    def __init__(self, name: str, chatId: int, ownerUserId: int, id: int, money: int, duration: int, workerUserId: int = None, deadline: str = None) -> None:
        self.id = id
        self.name = name
        self.chatId = chatId
        self.ownerUserId = ownerUserId
        self.money = money
        self.duration = duration
        self.workerUserId: int = workerUserId
        self.deadline: datetime.datetime = datetime.datetime.fromisoformat(deadline+'+03:00') if deadline else None
        

def FindTask(taskId: int) -> bool:
    return True if GetTask(taskId) else False

def GetAllTasks() -> list[Task]:
    responce:requests.Response = requests.get(
        url=f'http://localhost:8080/api/task/all',
        headers={"Content-Type": "application/json"})
    
    data: list[dict[str, Any]] = responce.json()
    tasks = [Task(**task) for task in data]

    return tasks

def GetFreeTasks() -> list[Task]:
    responce:requests.Response = requests.get(
        url=f'http://localhost:8080/api/task/free',
        headers={"Content-Type": "application/json"})

    data: list[dict[str, Any]] = responce.json()
    tasks = [Task(**task) for task in data]

    return tasks

def GetPlayerGivenTasks(chatId: int, userId: int) -> list[Task]:
    responce:requests.Response = requests.get(
        url=f'http://localhost:8080/api/task/person/{userId}/{chatId}',
        headers={"Content-Type": "application/json"})

    data: list[dict[str, Any]] = responce.json()
    tasks = [Task(**task) for task in data]

    return tasks

def GetPlayerTakenTasks(chatId: int, userId: int) -> list[Task]:
    responce:requests.Response = requests.get(
        url=f'http://localhost:8080/api/task/taken/{userId}/{chatId}',
        headers={"Content-Type": "application/json"})

    data: list[dict[str, Any]] = responce.json()
    tasks = [Task(**task) for task in data]

    return tasks

def GetTask(taskId: int) -> Task:
    for task in GetAllTasks():
        if taskId == task.id:
            return task
    return None

def TakeTask(player: Player.Player, task: Task, punish_job):

    deadline = datetime.datetime.now(tz.gettz("Europe/Moscow")) + datetime.timedelta(seconds=task.duration)
    task.deadline = deadline
    task.workerUserId = player.userId
    deadline = f"{deadline.year}-{deadline.month}-{deadline.day} {deadline.hour}:{deadline.minute}:{deadline.second}"

    response: requests.Response = requests.put(
        url=f'http://localhost:8080/api/task/update',
        json = {
            "id":task.id,
            "workerUserId":player.userId,
            "deadline": deadline
        },
        headers={"Content-Type": "application/json"})
    
    scheduler.add_job(punish_job, trigger='interval', seconds=task.duration, id=f'punish_{task.chatId}_{player.userId}_{task.id}', args=[task.chatId, task.workerUserId, task.id])

def RefuseTask(player: Player.Player, task: Task) -> bool:
    punished = False
    if (task.deadline - datetime.datetime.now(tz.gettz("Europe/Moscow"))) / datetime.timedelta(seconds=task.duration) < 0.7:
        scheduler.reschedule_job(f'punish_{task.chatId}_{task.workerUserId}_{task.id}', trigger='interval', seconds=1)
        punished = True 
    else:
        scheduler.remove_job(f'punish_{task.chatId}_{task.workerUserId}_{task.id}')

    response: requests.Response = requests.put(
        url=f'http://localhost:8080/api/task/update',
        json = {
            "id":task.id,
            "workerUserId":None,
            "deadline":None
        },
        headers={"Content-Type": "application/json"})
    
    task.deadline = None
    task.workerUserId = None
    return punished

def FreeTask(task: Task):
    response: requests.Response = requests.put(
        url=f'http://localhost:8080/api/task/update',
        json = {
            "id":task.id,
            "workerUserId":None,
            "deadline":None
        },
        headers={"Content-Type": "application/json"})
    
    task.deadline = None
    task.workerUserId = None

def AddTask(task: Task):

    response: requests.Response = requests.post(
        url=f'http://localhost:8080/api/task/create',
        json = {
            "name":task.name,
            "money":task.money,
            "duration":task.duration,
            "chatId":task.chatId,
            "ownerUserId":task.ownerUserId
        },
        headers={"Content-Type": "application/json"})

def DeleteTask(task: Task):

    responce:requests.Response = requests.delete(
        url=f'http://localhost:8080/api/task/delete/{task.id}',
        headers={"Content-Type": "application/json"})

def AcceptTask(task: Task):
    scheduler.remove_job(f'punish_{task.chatId}_{task.workerUserId}_{task.id}')
    DeleteTask(task)