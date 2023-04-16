from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from utils.scheduler import scheduler
import Classes.Player as Player
from utils.create_bot import bot, dp
import Classes.Quiz as Quiz
import random
import Classes.History as History
import handlers.achievement as AchievementHandler
from aiogram.types import InputFile, InputMediaPhoto

class FSMQuiz(StatesGroup):
    inQuiz = State()
    createQuizName = State()
    createQuizPhoto = State()
    questionText = State()
    questionAnswer = State()
    questionPhoto = State()
    questionContinue = State()


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
    if (Quiz.FindQuizInChat(call.message.chat.id)):
        await call.answer('Квиз уже проходит в чате')
        return
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
    if (quiz.image != ''):
        photo = open('./static/quizes/'+quiz.image, 'rb')
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

async def NextQuestion(ChatId: int):
    quiz: Quiz.QuizInChat = Quiz.GetQuizInChat(ChatId)
    await bot.send_message(chat_id=ChatId, text='Никто не ответил на вопрос.')
    quiz.number += 1
    if (quiz.number < len(quiz.questions)):
        question: Quiz.Question = quiz.questions[quiz.number]
        if (question.image != ''):
            photo = open('./static/quizes/' + question.image, 'rb')
            await bot.send_photo(chat_id=ChatId, caption=f'Минута на вопрос: {question.text}',photo=photo)
        else:
            await bot.send_message(chat_id=ChatId, text=f'Минута на вопрос: {question.text}')
        return
    
    text = 'Квиз закончен!\nТоп игроков по количеству ответов:'
    top = []
    for i in Player.GetAllPlayers(ChatId):
        st : FSMContext = dp.current_state(chat = i.chatId, user = i.userId)
        score = await st.get_data()
        top.append([i.name, score])
        statePlayer = await st.get_state()
        if statePlayer == FSMQuiz.inQuiz.state:
            await dp.current_state(chat = i.chatId, user = i.userId).set_state(None)
    Quiz.RemoveQuizInChat(quiz)
    top.sort(key=lambda x:x[1])
    for i in top[::-1]:
        text += f'\n{i[0]} - {i[1]}'
    await bot.send_message(chat_id=ChatId, text=text)
    scheduler.remove_job(f'quiz:{ChatId}')

async def StartQuiz(call: types.CallbackQuery, state: FSMContext):
    if not Player.FindPlayer(call.message.chat.id, call.from_user.id):
        await call.message.reply('Нужно зарегаться для такого')
        return
    if (Quiz.FindQuizInChat(call.message.chat.id)):
        await call.answer('Квиз уже проходит в чате')
        return
    try:
        id = int(call.data.replace("quizStart:",''))
    except:
        await call.answer()
        return
    
    quiz: Quiz.QuizInChat = Quiz.QuizInChat
    quiz.chatId = call.message.chat.id
    quiz.number = 0
    quiz.players = [Player.GetPlayer(call.message.chat.id, call.from_user.id)]
    quiz.questions = Quiz.GetQuestions(id)
    random.shuffle(quiz.questions)
    quiz.questions = quiz.questions[:10]
    if len(quiz.questions) == 0:
        await call.answer('Этот квиз ещё не готов')
        return
    await FSMQuiz.inQuiz.set()
    async with state.proxy() as data:
        data['inQuiz'] = 0
    Quiz.AddQuizInChat(quiz)
    question: Quiz.Question = quiz.questions[0]
    scheduler.add_job(NextQuestion, trigger='interval', seconds=60, jobstore='local', args=[call.message.chat.id], coalesce=True, id=f'quiz:{call.message.chat.id}')         
    
    qq = Quiz.GetQuiz(id)
    for i in Player.GetAllPlayers(call.message.chat.id):
        if (qq.image != ''):
            await bot.send_photo(chat_id=i.userId, 
                                caption=f'Сейчас проходит квиз:\n <b>{qq.name}</b>!\n Присоединяйтесь', 
                                photo=InputFile('./static/quizes/' + qq.image),
                                parse_mode='HTML')
        else:
            await bot.send_message(chat_id=i.userId, 
                                text=f'Сейчас проходит квиз:\n <b>{qq.name}</b>!\n Присоединяйтесь', 
                                parse_mode='HTML')
    
    
    
    
    if (question.image != ''):
        photo = InputFile('./static/quizes/' + question.image)
        await call.message.answer_photo(caption=f'Минута на вопрос: {question.text}',photo=photo)
    else:   
        await call.message.answer(text=f'Минута на вопрос: {question.text}')
    
    
    
    await call.answer()
    
async def AnswerQuestion(message: types.Message, state: FSMContext):
    quiz: Quiz.QuizInChat = Quiz.GetQuizInChat(message.chat.id)
    if (message.text.lower() == quiz.questions[quiz.number].answer.lower()):
        scheduler.remove_job(f'quiz:{message.chat.id}')
        scheduler.add_job(NextQuestion, trigger='interval', seconds=60, jobstore='local', args=[message.chat.id], coalesce=True, id=f'quiz:{message.chat.id}')
        await message.reply('Ответ правильный! \n<b>Заработано:</b>\n10 монет\n10 опыта', parse_mode='HTML')
        async with state.proxy() as data:
            data['inQuiz'] = data['inQuiz'] + 1
        quiz.number += 1
        player = Player.GetPlayer(message.chat.id, message.from_user.id)
        player.money += 10
        player.exp += 10
        history = History.GetHistory(message.chat.id, message.from_user.id)
        await AchievementHandler.SendAchievement(message.chat.id, message.from_user.id, history.UpdateHistory(totalMoney=10, totalExp=10))
        if (quiz.number < len(quiz.questions)):
            question: Quiz.Question = quiz.questions[quiz.number]
            if (question.image != ''):
                photo = open('./static/quizes/' + question.image, 'rb')
                await message.answer_photo(caption=f'Минута на вопрос: {question.text}',photo=photo)
            else:
                await message.answer(text=f'Минута на вопрос: {question.text}')
            return
        
        text = 'Квиз закончен!\nТоп игроков по ответам:'
        top = []
        for i in Player.GetAllPlayers(message.chat.id):
            st : FSMContext = dp.current_state(chat = i.chatId, user = i.userId)
            score = await st.get_data()
            statePlayer = await st.get_state()
            if statePlayer == FSMQuiz.inQuiz.state:
                top.append([i.name, score['inQuiz']])
                await st.set_data(None)
                await dp.current_state(chat = i.chatId, user = i.userId).set_state(None)
        Quiz.RemoveQuizInChat(quiz)
        top.sort(key=lambda x:x[1])
        for i in top[::-1]:
            text += f'\n{i[0]} - {i[1]}'
        await message.answer(text)
        scheduler.remove_job(f'quiz:{message.chat.id}')
    else:
        question: Quiz.Question = quiz.questions[quiz.number]
        if (question.image != ''):
                photo = open('./static/quizes/' + question.image, 'rb')
                await message.reply_photo(caption=f'Ответ неправильный😥\nВопрос: {question.text}', photo=photo)
        else:
            await message.reply(f'Ответ неправильный😥\nВопрос: {question.text}')
        

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
    await state.finish()
    await message.reply('Вы вышли из квиза')
    if len(quiz.players) == 0:
        Quiz.RemoveQuizInChat(quiz)
        scheduler.remove_job(f'quiz:{message.chat.id}')
        await message.answer('Квиз закончен! Все игроки вышли🥱')

async def CreateQuizName(message: types.Message, state: FSMContext):
    if not Player.FindPlayer(message.chat.id, message.from_user.id):
        await message.reply('Нужно зарегаться для такого')
        return
    await FSMQuiz.createQuizName.set()
    await message.answer('Вы начали создание квиза! Напишите название квиза')

async def CreateQuizPhoto(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['createQuizName'] = message.text
    await FSMQuiz.createQuizPhoto.set()
    await message.answer('Отправь фото, если не хочешь фото, просто ответь что-нибудь')

async def CreateQuizCreateWithoutPhoto(message: types.Message, state: FSMContext):
    id = len(Quiz.GetAllQuizes())
    quiz = Quiz.Quiz()
    quiz.id = id
    async with state.proxy() as data:
        quiz.name = data['createQuizName']
        data['createQuizName'] = quiz
    Quiz.AddQuiz(quiz)
    await FSMQuiz.questionText.set()
    await message.answer('Напиши текст первого вопроса')

async def CreateQuizCreateWithPhoto(message: types.Message, state: FSMContext):
    id = len(Quiz.GetAllQuizes())
    orig = f'./static/quizes/{id}_.png'
    await message.photo[-1].download(orig)
    quiz = Quiz.Quiz()
    quiz.id = id
    quiz.image = f'{id}_.png'
    async with state.proxy() as data:
        quiz.name = data['createQuizName']
        data['createQuizName'] = quiz
    Quiz.AddQuiz(quiz)
    await FSMQuiz.questionText.set()
    await message.answer('Напиши текст первого вопроса')

async def QuestionText(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['questionText'] = message.text
    await FSMQuiz.questionAnswer.set()
    await message.answer('Напиши ответ на вопрос')

async def QuestionAnswer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['questionAnswer'] = message.text
    await FSMQuiz.questionPhoto.set()
    await message.answer('Отправь фото. Если не хочешь фото, просто ответь что-нибудь')

async def QuestionCreateWithoutPhoto(message: types.Message, state: FSMContext):
    question = Quiz.Question()
    async with state.proxy() as data:
        question.quizId = data['createQuizName'].id
        question.id = len(Quiz.GetQuestions(question.quizId))
        question.text = data['questionText']
        question.answer = data['questionAnswer']
    Quiz.addQuestion(question)
    await FSMQuiz.questionContinue.set()
    await message.answer('Напиши + если хочешь ещё вопрос. Если нет, просто ответь что-нибудь')

async def QuestionCreateWithPhoto(message: types.Message, state: FSMContext):
    question = Quiz.Question()
    async with state.proxy() as data:
        question.quizId = data['createQuizName'].id
        question.id = len(Quiz.GetQuestions(question.quizId))
        question.text = data['questionText']
        question.answer = data['questionAnswer']
    orig = f'./static/quizes/{question.quizId}_{question.id}.png'
    await message.photo[-1].download(orig)
    question.image = f'{question.quizId}_{question.id}.png'
    Quiz.addQuestion(question)
    await FSMQuiz.questionContinue.set()
    await message.answer('Напиши + если хочешь ещё вопрос. Если нет, просто ответь что-нибудь')

async def QuestionContinue(message: types.Message, state: FSMContext):
    if (message.text != '+'):
        await state.finish()
        await message.answer('Вы закончили создание квиза')
        return
    await FSMQuiz.questionText.set()
    await message.answer('Напиши текст вопроса')

async def CancelQuizCreate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        quiz = Quiz.GetQuiz(data['createQuizName'].id)
    if quiz != None:
        Quiz.RemoveQuiz(quiz)
    await state.finish()
    await message.answer('Вы закончили создание квиза')


def register_handlers_quiz(dp: Dispatcher):
    dp.register_message_handler(QuizMenuStart, commands='quiz_list')
    dp.register_callback_query_handler(QuizPages, regexp='^myQuizPage:*')
    dp.register_callback_query_handler(StartQuiz, regexp='^quizStart:*', state=None)
    dp.register_callback_query_handler(ChoiceQuiz, regexp='^quiz:*')
    dp.register_message_handler(LeaveQuiz, state=FSMQuiz.inQuiz, commands='quiz_leave')
    dp.register_message_handler(AnswerQuestion, state=FSMQuiz.inQuiz)
    dp.register_message_handler(TakePartQuiz, commands='quiz_enter')
    dp.register_message_handler(CreateQuizName, commands='quiz_create')
    dp.register_message_handler(CancelQuizCreate, commands='quiz_create_cancel', state=[FSMQuiz.createQuizName, FSMQuiz.createQuizPhoto, FSMQuiz.questionAnswer, FSMQuiz.questionPhoto, FSMQuiz.questionText,FSMQuiz.questionContinue])
    dp.register_message_handler(CreateQuizPhoto, state=FSMQuiz.createQuizName)
    dp.register_message_handler(CreateQuizCreateWithPhoto, content_types=['photo'], state=FSMQuiz.createQuizPhoto)
    dp.register_message_handler(CreateQuizCreateWithoutPhoto, state=FSMQuiz.createQuizPhoto)
    dp.register_message_handler(QuestionText, state=FSMQuiz.questionText)
    dp.register_message_handler(QuestionAnswer, state=FSMQuiz.questionAnswer)
    dp.register_message_handler(QuestionCreateWithPhoto, content_types=['photo'], state=FSMQuiz.questionPhoto)
    dp.register_message_handler(QuestionCreateWithoutPhoto, state=FSMQuiz.questionPhoto)
    dp.register_message_handler(QuestionContinue, state=FSMQuiz.questionContinue)
    

    

            




