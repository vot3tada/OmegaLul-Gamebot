import requests
from typing import Any
from pathlib import Path
import configparser



FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

config = configparser.ConfigParser()
config.read(ROOT /'config.ini')
backhost = config['DEFAULT']['BACKHOST']
backport = config['DEFAULT']['BACKPORT']

class Achievement():

    def __init__(self, id: str, name: str, photo: str, condition: str, description: str):
        self.id: str = id
        self.name: str = name
        self.image: str = photo
        self.condition: int = condition
        self.description: str = description

class UserAchievement():
    
    def __init__(self, id: str, chatId: int, userId: int):
        self.chatId: int = chatId
        self.userId: int = userId
        self.achId: str = id

    def to_json(self) -> dict[str, Any]:
        json = {
            "achievementId": self.achId,
            "chatId": self.chatId,
            "userId": self.userId
        }
        return json


def GetUserAchivs(chatId: int, userId: int):
    responce:requests.Response = requests.get(
        url=f'http://{backhost}:{backport}/api/achievement/person/{chatId}/{userId}',
        headers={"Content-Type": "application/json"})
    
    if responce.status_code >= 400:
        return []
    
    achivs = [Achievement(**i) for i in responce.json()]

    return achivs

def AddUserAchiv(achiv: UserAchievement):
    responce:requests.Response = requests.post(
        url=f'http://{backhost}:{backport}/api/achievement/person/add',
        json = achiv.to_json(),
        headers={"Content-Type": "application/json"})
    
    if responce.status_code >= 400:
        return None

def GetAchievement(achId: int):
    responce:requests.Response = requests.get(
        url=f'http://{backhost}:{backport}/api/achievement/id/{achId}',
        headers={"Content-Type": "application/json"})
    
    if responce.status_code >= 400:
        return []
    
    achiv = Achievement(**responce.json())

    return achiv

def Check(achId: int, condition: int):
    return GetAchievement(achId).condition <= condition
    

