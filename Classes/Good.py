from typing import Any, Union
import requests

class Good():
    
    def __init__(self, 
                 name: str,
                 id: int,
                 price: int,
                 description: str,
                 effects: dict[str, Any],
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
        url=f'http://localhost:8080/api/item/all',
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
        url=f'http://localhost:8080/api/item/id/{id}',
        headers={"Content-Type": "application/json"})

    if not responce.ok:
        return None
    
    data: list[dict[str, Any]] = responce.json()
    good = Good(**data)

    return good

