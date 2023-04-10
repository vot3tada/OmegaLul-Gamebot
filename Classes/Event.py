from ctypes import Union
from datetime import datetime, date, time
from utils.scheduler import scheduler

class Event():
    id = 0
    name = ''
    datetime = datetime.today()
    players = []
    creator = ''
    
    
    def __init__(self):
        self.id = datetime.today()
        self.datetime = datetime.today()
        self.players = []

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