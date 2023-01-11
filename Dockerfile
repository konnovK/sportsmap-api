FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN wget "https://storage.yandexcloud.net/cloud-certs/CA.pem"

COPY . .

CMD [ "python3", "main.py"]