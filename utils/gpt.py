import openai
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
token=config['DEFAULT']['CHATGPTTOKEN']
openai.api_key = token

def talk_to_bot1(messagetext: str):
    

    model_engine = "text-davinci-003"
    prompt = messagetext
    # генерируем ответ
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=2048,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # выводим ответ
    return completion.choices[0].text

def talk_to_bot2(messagetext: str):
    messages = []  
    prompt = 'Ответь как робот, отвечай от имени ОмегаЛюль, в начало ответа подставь включение системы, подключение к базе знаний и в этом духе, в конце наоборот отключение системы: '+messagetext
    #prompt = messagetext
    messages.append(
        {
            'role':'user',
            'content':prompt
        })    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = messages)
    
    response = completion['choices'][0]['message']['content']
    return response