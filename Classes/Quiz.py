from Classes.Player import Player

class Quiz():
    def __init__(self):
        self.id = 0
        self.name: str = ''
        self.players: list[Player] = []


class Question():
    def __init__(self):
        self.id = 0
        self.text = ''
        self.answer = ''
        self.image = ''
        self.quizId = 0
        
Chats: list[int] = []
Quizes: list[Quiz] = []
Questions: list[Question] = []

def AddQuiz(quiz: Quiz):
    Quizes.append(quiz)

def GetQuiz(id: int):
    q = [i for i in Quizes if i.id == id]
    return q[0] if len(q) != 0 else None

def addQuestion(question: Question):
    Questions.append(question)

def GetAllQuizes() -> list[Quiz]:
    return Quiz.copy()

def getQuetions(quizId: int):
    return [i for i in Questions if i.quizId == quizId]