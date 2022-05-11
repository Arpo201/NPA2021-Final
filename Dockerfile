FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirement.txt .
RUN pip install -r requirement.txt

COPY 62070174-bot.py .

ENTRYPOINT [ "python", "62070174-bot.py" ]
