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
        50,
        40
     ),
     Work( 
        1,
        'Подрабатывать у Задорожного плюсовиком',
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


