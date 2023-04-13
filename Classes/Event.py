from ctypes import Union
from datetime import datetime, date, time
from utils.scheduler import scheduler
from Classes.Player import Player

class Event():

 
    def __init__(self):
        self.id = datetime.today()
        self.datetime = datetime.today()
        self.players: list[Player] = []
        self.creator: Player = None
        self.name: str = ''

Events: list[Event] = []

def GetEvent(id: int):
    for i in Events:
        if (i.id == id):
            return i
    return None

def GetCount() -> int:
    jobs = scheduler.get_jobs()
    return len([i for i in jobs if i.id[0] == 'e'])

def GetAllEvents() -> list[Event]:
    return Events.copy()

def AddEvent(event : Event):
    Events.append(event)