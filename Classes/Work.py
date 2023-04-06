class Work():

    def __init__(self, id: int,  name :str, levelRequired: int, expReward: int, moneyReward: int):
        self.id = id
        self.name = name
        self.levelRequired = levelRequired
        self.expReward = expReward
        self.moneyReward = moneyReward

#Имя работы должно начинаться с глагола в инфинитиве
Works : list[Work] = [
    Work( 
        0,
        'Учить детей питону в шараге',
        0,
        100,
        200
     ),
     Work( 
        1,
        'Подрабатывать у Задорожного плюсовиком',
        2,
        200,
        400
     )
]   


