import Classes.Player as Player
from utils.create_bot import dp, bot
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

class Achievement():

    def __init__(self):
        self.id: int = 0
        self.name: str = ''
        self.image: str = ''
        self.condition: int = 0
        self.description: str = ''

class UserAchievement():
    
    def __init__(self):
        self.id: int = 0
        self.chatId: int = 0
        self.userId: int = 0
        self.achId: int = 0

userAchiv: list[UserAchievement] = []

def GetUserAchivs(chatId: int, userId: int):
    return [i for i in userAchiv if i.chatId == chatId and i.userId == userId]

def AddUserAchiv(achiv: UserAchievement):
    userAchiv.append(achiv)

ach1 = Achievement()
ach1.id = 0
ach1.name = 'Пончик'
ach1.image = (ROOT / '0.jpg').__str__()
ach1.condition = 20
ach1.description = 'Своим трудом заработать 100000 денег'

ach2 = Achievement()
ach2.id = 1
ach2.name = 'Старец'
ach2.image = (ROOT / '1.jpg').__str__()
ach2.condition = 20
ach2.description = 'Заработать 100000 опыта'

ach3 = Achievement()
ach3.id = 2
ach3.name = 'Крутите барабан'
ach3.image = (ROOT / '2.jpg').__str__()
ach3.condition = 100
ach3.description = 'Ответить на 100 вопросов'

ach4 = Achievement()
ach4.id = 3
ach4.name = 'Ты знаешь Тайлера?'
ach4.image = (ROOT / '3.jpg').__str__()
ach4.condition = 100
ach4.description = 'Поучавствовать в 100 битвах'

ach5 = Achievement()
ach5.id = 4
ach5.name = 'Баки'
ach5.image = (ROOT / '4.jpg').__str__()
ach5.condition = 100
ach5.description = 'Победить 100 битв'

ach6 = Achievement()
ach6.id = 5
ach6.name = 'Искатель приключений'
ach6.image = (ROOT / '5.jpg').__str__()
ach6.condition = 1
ach6.description = 'Победить босса'

ach7 = Achievement()
ach7.id = 6
ach7.name = 'Барахольщик'
ach7.image = (ROOT / '6.jpg').__str__()
ach7.condition = 100
ach7.description = 'Купить 100 предметов'

ach8 = Achievement()
ach8.id = 7
ach8.name = 'Ривийский акцент'
ach8.image = (ROOT / '7.jpg').__str__()
ach8.condition = 100
ach8.description = 'Взять 100 заданий с доски'

ach9 = Achievement()
ach9.id = 8
ach9.name = 'Миска риса'
ach9.image = (ROOT / '8.jpg').__str__()
ach9.condition = 10
ach9.description = 'Выполнить 10 заданий с доски'

ach10 = Achievement()
ach10.id = 9
ach10.name = 'Шляпа'
ach10.image = (ROOT / '9.jpg').__str__()
ach10.condition = 10
ach10.description = 'Прошляпить выполнение 10 заданий с доски'

ach11 = Achievement()
ach11.id = 10
ach11.name = 'Коллектор-звонилка'
ach11.image = (ROOT / '10.jpg').__str__()
ach11.condition = 1
ach11.description = 'Победить коллектора'

ach12 = Achievement()
ach12.id = 11
ach12.name = 'Тамада'
ach12.image = (ROOT / '11.jpg').__str__()
ach12.condition = 10
ach12.description = 'Провести 10 мероприятий'

ach13 = Achievement()
ach13.id = 12
ach13.name = 'Таксист'
ach13.image = (ROOT / '12.jpg').__str__()
ach13.condition = 10
ach13.description = 'Посетить 10 мероприятий'

ach14 = Achievement()
ach14.id = 13
ach14.name = 'Футболист'
ach14.image = (ROOT / '13.jpg').__str__()
ach14.condition = 10
ach14.description = 'Выгнать 10 посетителей'

ach15 = Achievement()
ach15.id = 14
ach15.name = 'Сопляк'
ach15.image = (ROOT / '14.jpg').__str__()
ach15.condition = 1
ach15.description = 'Сбежать с битвы'

Achievements = [ach1, ach2, ach3, ach4, ach5, ach6, ach7, ach8, ach9, ach10, ach11, ach12, ach13, ach14, ach15]

def GetAchievement(achId: int):
    return [i for i in Achievements if i.id == achId][0]

def Check(achId: int, condition: int):
    return [i for i in Achievements if i.id == achId][0].condition <= condition
    

