from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from utils.scheduler import scheduler
import Classes.Player as Player
from utils.create_bot import bot, dp
import Classes.Quiz as Quiz

class FSMQuiz(FSMContext):
    inQuiz = State()
    numberOfQuestion = State()
    createQuiz = State()
    addPhoto = State()
    players = State()
