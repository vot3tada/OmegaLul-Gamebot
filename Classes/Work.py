class Work():
    name :str
    levelRequired :int 
    expReward : int
    moneyReward :int

    def __init__(self, name :str, levelRequired: int, expReward: int, moneyReward: int):
        self.name = name
        self.levelRequired = levelRequired
        self.expReward = expReward
        self.moneyReward = moneyReward

#Имя работы должно начинаться с глагола в инфинитиве
Works : list[Work] = [
    Work( 
        'Учить детей питону в шараге',
        0,
        100,
        200
     ),
     Work( 
        'Подрабатывать у Задорожного плюсовиком',
        2,
        200,
        400
     )
]   


