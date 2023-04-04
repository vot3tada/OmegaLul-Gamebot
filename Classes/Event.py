from ctypes import Union
from datetime import datetime, date, time

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

def GetAllEvents() -> list[Event]:
    return Events.copy()

def AddEvent(event : Event):
    Events.append(event)