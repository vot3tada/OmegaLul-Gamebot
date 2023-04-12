from Classes.Player import Player

class Quiz():
    def __init__(self):
        self.id: int = 0
        self.name: str = ''
        self.image: str = ''


class Question():
    def __init__(self):
        self.id: int = 0
        self.text: str = ''
        self.answer: str = ''
        self.image: str = ''
        self.quizId: int = 0

class QuizInChat():#этот класс в бд не надо
    def __init__(self):
        self.chatId: int = 0
        self.number: int = 0
        self.questions: list[Question] = []
        self.players: list[Player] = []
        
quiz = Quiz()
quiz.name = 'Евагелион еее'
quiz.photo = '1.png'
quiz.id = 1

question1 = Question()
question1.text = 'Это кто?'
question1.answer = 'Мисато'
question1.image = '2.png'
question1.quizId = 1
question2 = Question()
question2.text = 'И что она пьет?'
question2.answer = 'Ебису'
question2.quizId = 1


Chats: list[QuizInChat] = []#Это тоже в бд не надо
Quizes: list[Quiz] = [quiz]
Questions: list[Question] = [question1, question2]

def AddQuizInChat(quiz: QuizInChat):
    Chats.append(quiz)

def GetQuizInChat(chatId: int):
    for i in Chats:
        if i.chatId == chatId:
            return i
    return None

def FindQuizInChat(chatId: int):
    return chatId in [i.id for i in Chats]

def RemoveQuizInChat(quiz: QuizInChat):
    Chats.remove(quiz)

def AddQuiz(quiz: Quiz):
    Quizes.append(quiz)

def GetQuiz(id: int):
    q = [i for i in Quizes if i.id == id]
    return q[0] if len(q) != 0 else None

def addQuestion(question: Question):
    Questions.append(question)

def GetAllQuizes() -> list[Quiz]:
    return Quizes.copy()

def getQuestions(quizId: int):
    return [i for i in Questions if i.quizId == quizId]
