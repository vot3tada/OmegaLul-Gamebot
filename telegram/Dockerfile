FROM python:3.9-slim
RUN apt update
RUN apt -y install libpq-dev
RUN apt -y install cmake
RUN apt -y install g++
RUN apt-get -y install libgl1 libglib2.0-0 libsm6 libxrender1 libxext6
WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "bot_telegram.py"]