import Classes.Player as Player

class Good():
    
    name = ''
    price = 0
    def Effect():
        pass

class HPPotion(Good):

    def __init__(self):
        self.name = 'Хилка'
        self.price = 50

    def Effect(player: Player):
        player.hp += 50
        if player.hp > 100: player.hp = 100


class LuckPotion(Good):

    def __init__(self):
        self.name = 'Немного удачи'
        self.price = 200

    def Effect(player: Player):
        player.luckMultiply *= 2

class DamagePotion(Good):

    def __init__(self):
        self.name = 'Сила++'
        self.price = 200

    def Effect(player: Player):
        player.damageMultiply *= 2

    
