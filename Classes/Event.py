from ctypes import Union
from datetime import datetime, date, time
from utils.scheduler import scheduler
from Classes.Player import Player

class Event():

 
    def __init__(self):
        self.id = 0
        self.chatId = 0
        self.name: str = ''
        self.datetime = datetime.today()
        self.players: list[Player] = []
        self.userId = 0
        

Events: list[Event] = []

def GetEvent(id: int):
    for i in Events:
        if (i.id == id):
            return i
    return None

def GetCount() -> int:
    jobs = scheduler.get_jobs()
    return len([i for i in jobs if i.id[0] == 'e'])

def GetAllEvents(chatId) -> list[Event]:
    return [i for i in Events if i.chatId == chatId]

def AddEvent(event : Event):
    Events.append(event)