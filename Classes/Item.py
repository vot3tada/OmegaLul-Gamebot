from typing import Union
from Classes.Good import Good

class HPPotion(Good):

    name : str = 'Жигули Барное'
    id : str = 'HPPotion'
    price : int = 50
    description : str = 'Хиляет перса'
    duration : int = 0

    effects: dict[str, float] = {
        'hp' : 50
    }


class LuckPotion(Good):

    name : str = 'Немного удачи'
    id : str = 'LuckPotion'
    price : int = 200
    description : str = 'Увеличивает удачу'

    effects: dict[str, float] = {
        'luckMultiply' : 0.5
    }
    

class DamagePotion(Good):

    name : str = 'Немного дамага'
    id : str = 'DamagePotion'
    price : int = 200
    description : str = 'Увеличивает силу'

    effects: dict[str, float] = {
        'damageMultiply' : 0.5
    }


Items : dict[str, Good] = {
    HPPotion.id : HPPotion(),
    LuckPotion.id : LuckPotion(),
    DamagePotion.id : DamagePotion(),
}

def FindItem(id: str) -> bool:
    for item in Items.values():
        if item.id == id:
            return True
    return False

def GetItem(id: str) -> Union[Good, None]:
    return Items[id]

    
