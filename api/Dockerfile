FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN wget "https://storage.yandexcloud.net/cloud-certs/CA.pem"

COPY . .

ARG API_PORT
EXPOSE ${API_PORT}

CMD [ "python3", "main.py"]