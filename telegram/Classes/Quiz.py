import Classes.Player as Player
from typing import Any
import requests
from pathlib import Path
import configparser

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

config = configparser.ConfigParser()
config.read(ROOT /'config.ini')
backhost = config['DEFAULT']['BACKHOST']
backport = config['DEFAULT']['BACKPORT']

class Quiz():
    def __init__(self, id: int, name: str, photo: str):
        self.id: int = id
        self.name: str = name
        self.image: str = photo
    
    def to_json(self) -> dict[str, Any]:
        json = {
            "name": self.name,
            "photo": self.image
        }
        return json


class Question():
    def __init__(self, id: int, text: str, answer: str, photo: str, quizId: int):
        self.id: int = id
        self.text: str = text
        self.answer: str = answer
        self.image: str = photo
        self.quizId: int = quizId
    
    def to_json(self) -> dict[str, Any]:
        json = {
            "text": self.text,
            "photo": self.image,
            "answer": self.answer,
            "quizId": self.quizId
        }
        return json

class QuizInChat():#этот класс в бд не надо
    def __init__(self):
        self.chatId: int = 0
        self.number: int = 0
        self.questions: list[Question] = []
        self.players: list[Player.Player] = []
        


Chats: list[QuizInChat] = []#Это тоже в бд не надо

def AddQuizInChat(quiz: QuizInChat):
    Chats.append(quiz)

def GetQuizInChat(chatId: int):
    for i in Chats:
        if i.chatId == chatId:
            return i
    return None

def FindQuizInChat(chatId: int):
    return chatId in [i.chatId for i in Chats]

def RemoveQuizInChat(quiz: QuizInChat):
    Chats.remove(quiz)

def AddQuiz(quiz: Quiz):
    responce:requests.Response = requests.post(
        url=f'http://{backhost}:{backport}/api/quiz/create',
        json = quiz.to_json(),
        headers={"Content-Type": "application/json"})
    
    if responce.status_code >= 400:
        return None
    
    quiz: Quiz = Quiz(**responce.json())
    return quiz

def GetQuiz(id: int):
    responce:requests.Response = requests.get(
        url=f'http://{backhost}:{backport}/api/quiz/id/{id}',
        headers={"Content-Type": "application/json"})
    
    if responce.status_code >= 400:
        return None
    
    quiz: Quiz = Quiz(responce.json()['id'], responce.json()['name'], responce.json()['photo'])
    return quiz

def addQuestion(question: Question):
    responce:requests.Response = requests.post(
        url=f'http://{backhost}:{backport}/api/quiz/add/question',
        json = question.to_json(),
        headers={"Content-Type": "application/json"})
    
    if responce.status_code >= 400:
        return None

def GetAllQuizes() -> list[Quiz]:
    responce:requests.Response = requests.get(
        url=f'http://{backhost}:{backport}/api/quiz/all',
        headers={"Content-Type": "application/json"})
    
    if responce.status_code >= 400:
        return []
    
    events = [Quiz(**i) for i in responce.json()]

    return events

def GetQuestions(quizId: int):
    responce:requests.Response = requests.get(
        url=f'http://{backhost}:{backport}/api/quiz/id/{quizId}',
        headers={"Content-Type": "application/json"})
    
    if responce.status_code >= 400:
        return []
    
    questions: list[Question] = [Question(**i) for i in responce.json()['questions']]
    return questions
    


def RemoveQuiz(quizId: int):
    responce:requests.Response = requests.delete(
        url=f'http://{backhost}:{backport}/api/quiz/delete/{quizId}',
        headers={"Content-Type": "application/json"})
    
    if responce.status_code >= 400:
        return None
