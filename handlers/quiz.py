from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from utils.scheduler import scheduler
import Classes.Player as Player
from utils.create_bot import bot, dp
import Classes.Quiz as Quiz
import os

class FSMQuiz(StatesGroup):
    inQuiz = State()
    numberOfQuestion = State()
    createQuiz = State()
    addPhoto = State()
    players = State()


async def QuizMenuStart(message : types.Message):
    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Нужно зарегаться для такого')
        return

    quizes: list[Quiz.Quizes] = Quiz.GetAllQuizes()
    replytext = f'<b>Список квизов</b>:\n'
    keyboard = types.InlineKeyboardMarkup()
    for quiz in quizes[:5]:
        keyboard.add(
            types.InlineKeyboardButton(text=quiz.name, callback_data=f'quiz:{quiz.id}')
        )
    if len(quizes) > 5:
        buttons: list[types.InlineKeyboardButton] = []
        buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
        buttons.append(types.InlineKeyboardButton(text='1', callback_data="@$^"))
        buttons.append(types.InlineKeyboardButton(text='След. ', callback_data=f'myQuizPage:{message.chat.id}_{message.from_user.id}_1'))
        keyboard.row(*buttons)

    await message.answer(
        text=replytext,
        reply_markup=keyboard,
        parse_mode='HTML'
    )

async def QuizPages(call: types.CallbackQuery):
    chatId, userId, page = call.data.replace("myQuizPage:",'').split('_')
    if call.message.chat.id != int(chatId) or call.from_user.id != int(userId):
        await call.answer('Это не ваш список')
        return
    try:
        page = int(page)
    except:
        await call.answer()
        return
    player: Player.Player = Player.GetPlayer(int(chatId), int(userId))
    quizes: list[Quiz.Quizes] = Quiz.GetAllQuizes()
    keyboard = types.InlineKeyboardMarkup()
    for quiz in quizes[page*5:page*5+5]:
        keyboard.add(
            types.InlineKeyboardButton(text=quiz.name, callback_data=f'quiz:{quiz.id}')
        )
    if len(quizes) > 5:
        buttons: list[types.InlineKeyboardButton] = []
        if page:
            buttons.append(types.InlineKeyboardButton(text='Пред. ', callback_data=f'myQuizPage:{player.chatId}_{player.userId}_{page-1}'))
        else:
            buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
        buttons.append(types.InlineKeyboardButton(text=page+1, callback_data="@$^"))
        if len(quizes) > page*5 + 5:
            buttons.append(types.InlineKeyboardButton(text='След. ', callback_data=f'myQuizPage:{player.chatId}_{player.userId}_{page+1}'))
        else:
            buttons.append(types.InlineKeyboardButton(text='    ', callback_data=f'@$^'))
        keyboard.row(*buttons)

    await call.message.edit_text(
        reply_markup=keyboard,
        text= f'<b>Список квизов</b>:\n',
        parse_mode='HTML'
    )
    await call.answer()

async def ChoiceQuiz(call: types.CallbackQuery):
    id = call.data.replace("quiz:",'')
    try:
        id = int(id)
    except:
        await call.answer()
        return
    quiz: Quiz.Quiz = Quiz.GetQuiz(id)
    if not quiz:
        await call.answer('Квиза не существует')
        return
        
    replyText = f'<b>{quiz.name}</b>'
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Начать', callback_data=f'quizStart:{id}'))
    if (quiz.photo != ''):
        photo = open('./static/quizes/'+quiz.photo, 'rb')
        await call.message.answer_photo(
            caption=replyText,
            photo=photo,
            reply_markup=keyboard,
            parse_mode='HTML'
        )
    else:
        await call.message.answer(
            text=replyText,
            reply_markup=keyboard,
            parse_mode='HTML'
        )
    await call.answer()

async def StartQuiz(call: types.CallbackQuery, state: FSMContext):
    if not Player.FindPlayer(call.message.chat.id, call.from_user.id):
        await call.message.reply('Нужно зарегаться для такого')
        return
    if (Quiz.FindQuizInChat(call.message.chat.id)):
        await call.message.answer('Квиз уже проходит в чате')
        return
    try:
        id = int(call.data.replace("quizStart:",''))
    except:
        await call.answer()
        return
    await FSMQuiz.inQuiz.set()
    async with state.proxy() as data:
        data['inQuiz'] = 0
    quiz: Quiz.QuizInChat = Quiz.QuizInChat
    quiz.chatId = call.message.chat.id
    quiz.number = 0
    quiz.players = [Player.GetPlayer(call.message.chat.id, call.from_user.id)]
    quiz.questions = Quiz.getQuestions(id)
    Quiz.AddQuizInChat(quiz)
    question: Quiz.Question = quiz.questions[0]
    if (question.image != ''):
        photo = open('./static/quizes/' + question.image, 'rb')
        await call.message.answer_photo(caption=f'Вопрос: {question.text}',photo=photo)
    else:
        await call.message.answer(text=f'Вопрос: {question.text}')
    await call.answer()

async def AnswerQuestion(message: types.Message, state: FSMContext):
    quiz: Quiz.QuizInChat = Quiz.GetQuizInChat(message.chat.id)
    if (message.text.lower() == quiz.questions[quiz.number].answer.lower()):
        await message.reply('Ответ правильный!')
        async with state.proxy() as data:
            data['inQuiz'] = data['inQuiz'] + 1
        #Можно уже здесь добавлять деньги/опыт
        quiz.number += 1
        if (quiz.number < len(quiz.questions)):
            question: Quiz.Question = quiz.questions[quiz.number]
            if (question.image != ''):
                photo = open('./static/quizes/' + question.image, 'rb')
                await message.answer_photo(caption=f'Вопрос: {question.text}',photo=photo)
            else:
                await message.answer(text=f'Вопрос: {question.text}')
            return
        
        await message.answer('Квиз закончен!')
        for i in Player.GetAllPlayers(message.chat.id):
            st : FSMContext = dp.current_state(chat = i.chatId, user = i.userId)
            statePlayer = await st.get_state()
            if statePlayer == FSMQuiz.inQuiz.state:
                await dp.current_state(chat = i.chatId, user = i.userId).set_state(None)
        Quiz.RemoveQuizInChat(quiz)
    else:
        await message.reply('Ответ неправильный😥')

async def TakePartQuiz(message: types.Message, state: FSMContext):
    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Нужно зарегаться для такого')
        return
    quiz: Quiz.QuizInChat = Quiz.GetQuizInChat(message.chat.id)
    if quiz == None:
        await message.answer('Сейчас не проходит квиз в чате!')
        return
    quiz.players.append(Player.GetPlayer(message.chat.id, message.from_user.id))
    await FSMQuiz.inQuiz.set()
    async with state.proxy() as data:
        data['inQuiz'] = 0
    await message.reply('Вы участвуете в квизе')

async def LeaveQuiz(message: types.Message, state: FSMContext):
    quiz: Quiz.QuizInChat = Quiz.GetQuizInChat(message.chat.id)
    eventUserId = [i.userId for i in quiz.players]
    quiz.players.pop(eventUserId.index(message.from_user.id))
    #а можно и здесь выдавать награду
    await state.finish()
    await message.reply('Вы вышли из квиза')

    if len(quiz.players) == 0:
        Quiz.RemoveQuizInChat(quiz)
        await message.answer('Квиз закончен! Все игроки вышли🥱')

def register_handlers_quiz(dp: Dispatcher):
    dp.register_message_handler(QuizMenuStart, commands='quiz_list')
    dp.register_callback_query_handler(QuizPages, regexp='^myQuizPage:*')
    dp.register_callback_query_handler(StartQuiz, regexp='^quizStart:*', state=None)
    dp.register_callback_query_handler(ChoiceQuiz, regexp='^quiz:*')
    dp.register_message_handler(LeaveQuiz, state=FSMQuiz.inQuiz, commands='quiz_leave')
    dp.register_message_handler(AnswerQuestion, state=FSMQuiz.inQuiz)
    dp.register_message_handler(TakePartQuiz, commands='quiz_enter')
    

            




