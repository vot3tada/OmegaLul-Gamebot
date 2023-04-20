from typing import Any, Union
import requests
from pathlib import Path
import configparser

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

config = configparser.ConfigParser()
config.read(ROOT /'config.ini')
backhost = config['DEFAULT']['BACKHOST']
backport = config['DEFAULT']['BACKPORT']

class Good():
    
    def __init__(self, 
                 name: str,
                 id: int,
                 price: int,
                 description: str,
                 effects: list[dict[str, Any]],
                 duration: int = 10
                 ) -> None:
        self.name = name
        self.id = id
        self.price = price
        self.description = description
        self.effects = effects
        self.duration = duration

def GetAllItems() -> Union[list[Good], None]:

    responce:requests.Response = requests.get(
        url=f'http://{backhost}:{backport}/api/item/all',
        headers={"Content-Type": "application/json"})

    if not responce.ok:
        return None
    
    data: list[dict[str, Any]] = responce.json()
    goods = [Good(**good) for good in data]

    return goods

def FindItem(id: str) -> bool:
    for item in GetAllItems():
        if item.id == id:
            return True
    return False
        
def GetItem(id: int) -> Union[Good,None]:
    responce:requests.Response = requests.get(
        url=f'http://{backhost}:{backport}/api/item/id/{id}',
        headers={"Content-Type": "application/json"})

    if not responce.ok:
        return None
    
    data: list[dict[str, Any]] = responce.json()
    good = Good(**data)

    return good


