from datetime import datetime
from typing import Any
from utils.scheduler import scheduler
import  Classes.Player as Player
import requests
from dateutil import tz
from pathlib import Path
import configparser

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

config = configparser.ConfigParser()
config.read(ROOT /'config.ini')
backhost = config['DEFAULT']['BACKHOST']
backport = config['DEFAULT']['BACKPORT']

class Member():
        def __init__(self, creator: bool, chatId: int, userId: int) -> None:
            self.creator = creator
            self.chatId = chatId
            self.userId = userId

        def to_json(self) -> dict[str, Any]:
            json = {
                "creator": self.creator,
                "chatId": self.chatId,
                "userId": self.userId
            }
            return json
        

class Event():
    def __init__(self, id, name, startedAt, members):
        self.id = id
        self.name: str = name
        
        dt = datetime.strptime(startedAt, '%Y-%m-%d %H:%M:%S')
        self.datetime = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, tzinfo=tz.gettz("Europe/Moscow"))
        mb = [Member(**i) for i in members] if members != None else []
        self.players = [Player.GetPlayer(i.chatId, i.userId) for i in mb]
        if (len(mb) > 0):
            self.chatId = mb[0].chatId
            self.userId = [i.userId for i in mb if i.creator == True][0]
        else:
            self.chatId = 0
            self.userId = 0

    def to_json(self) -> dict[str, Any]:
        json = {
            "name": self.name,
            "startedAt": str(self.datetime).replace('+03:00',''),
            "chatId": self.chatId,
            "userId": self.userId
        }
        return json
        

Events: list[Event] = []

def GetEvent(id: int):
    responce:requests.Response = requests.get(
        url=f'http://{backhost}:{backport}/api/event/id/{id}',
        headers={"Content-Type": "application/json"})
    
    if responce.status_code >= 400:
        return None
    
    event: Event = Event(**responce.json())
    return event

def GetCount() -> int:
    jobs = scheduler.get_jobs()
    return len([i for i in jobs if i.id[0] == 'e'])

def GetAllEvents(chatId) -> list[Event]:
    responce:requests.Response = requests.get(
        url=f'http://{backhost}:{backport}/api/event/chat/{chatId}',
        headers={"Content-Type": "application/json"})
    
    if responce.status_code >= 400:
        return []
    
    events = [Event(**i) for i in responce.json()]

    return events

def AddEvent(event : Event):
    responce:requests.Response = requests.post(
        url=f'http://{backhost}:{backport}/api/event/create',
        json = event.to_json(),
        headers={"Content-Type": "application/json"})
    
    if responce.status_code >= 400:
        return None
    
    event: Event = Event(**responce.json())
    return event
    
def AddUser(eventId: int, userId: int, chatId: int):
    member = {
        'id' : eventId,
        'chatId' : chatId,
        'userId' : userId
    }
    responce:requests.Response = requests.post(
        url=f'http://{backhost}:{backport}/api/event/add-member',
        json = member,
        headers={"Content-Type": "application/json"})

def KickUser(eventId: int, userId: int, chatId: int):
    member = {
        'id' : eventId,
        'chatId' : chatId,
        'userId' : userId
    }
    responce:requests.Response = requests.delete(
        url=f'http://{backhost}:{backport}/api/event/delete-member',
        json = member,
        headers={"Content-Type": "application/json"})
    
def RemoveEvent(eventId: int):
    responce:requests.Response = requests.delete(
        url=f'http://{backhost}:{backport}/api/event/delete/{eventId}',
        headers={"Content-Type": "application/json"})