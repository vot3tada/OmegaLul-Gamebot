import openai
import configparser

def talk_to_bot(messagetext: str):
    config = configparser.ConfigParser()
    config.read('config.ini')
    token=config['DEFAULT']['CHATGPTTOKEN']

    model_engine = "text-davinci-003"
    prompt = messagetext

    openai.api_key = token

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