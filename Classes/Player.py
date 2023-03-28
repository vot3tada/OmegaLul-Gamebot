from pickle import load, dump

class Player():

    name = ''
    exp = 0
    money = 1000
    photo = ''
    inventory = []

    luck = 0.2
    luckMultiply = 1

    hp = 100
    damage = 25
    damageMultiply = 1

    def __init__(self):
        self.inventory = []

Players :dict[str, Player] = load(open("users.pkl","rb"))

def SaveUsers():
    with open("users.pkl", "wb") as file:
        dump(Players, file)


