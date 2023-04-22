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

class Work():

    def __init__(self, id: int,  name :str, levelRequired: int, expReward: int, moneyReward: int):
        self.id = id
        #Имя работы должно начинаться с глагола в инфинитиве
        self.name = name
        self.levelRequired = levelRequired
        self.expReward = expReward
        self.moneyReward = moneyReward

def GetAllWork() -> list[Work]:
    responce:requests.Response = requests.get(
        url=f'http://{backhost}:{backport}/api/work/all',
        headers={"Content-Type": "application/json"})

    if not responce.ok:
        return None
    
    data: list[dict[str, Any]] = responce.json()
    works = [Work(**work) for work in data]
    return works

def GetWork(id: int) -> Work:
   works = GetAllWork()
   for work in works:
      if work.id == id:
         return work

Works : list[Work] = [
    Work( 
        0,
        'Учить детей питону в шараге',
        0,
        50,
        40
     ),
     Work( 
        1,
        'Подрабатывать у препода плюсовиком',
        4,
        120,
        80
     ),
     Work( 
        2,
        'Формашлепить стажировские задания',
        8,
        150,
        110
     ),
     Work( 
        3,
        'Ревьюить код шушпенчиков',
        12,
        180,
        130
     ),
     Work( 
        4,
        'Потаунтить Ривендера',
        18,
        200,
        180
     )
]   


