FROM python:3

WORKDIR /usr/src/app

COPY requirements/. requirements/
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./telegram_bot.py" ]