FROM python:3.9-slim
RUN apt update && \
    apt -y install libpq-dev && \
    apt -y install cmake && \
    apt -y install g++ && \
    apt-get -y install libgl1 libglib2.0-0 libsm6 libxrender1 libxext6

WORKDIR /app

ADD ./requirements.txt /app/requirements.txt

RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt

COPY . /app
RUN chmod a+x "./wait-for-it.sh"

CMD ["./wait-for-it.sh", "gamebot-back:8080", "--timeout=60", "--", "python3", "bot_telegram.py"]