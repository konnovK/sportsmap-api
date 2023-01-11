FROM python:3.11

WORKDIR /app

EXPOSE ${API_PORT}

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN wget "https://storage.yandexcloud.net/cloud-certs/CA.pem"

COPY . .


CMD [ "python3", "main.py"]