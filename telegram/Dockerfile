FROM python:3.9-slim
RUN apt update && apt -y install libpq-dev\
    && apt -y install cmake && apt -y install g++\
    && apt-get -y install libgl1 libglib2.0-0 libsm6 libxrender1 libxext6

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "bot_telegram.py"]