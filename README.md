# SportsMap API

Бэкенд для веб приложения с картой спортивных объектов СПб.

### SSL для базы данных

В корне проекта необходимо положить файл `CA.pem`, в котором
находится ssl сертификат для доступа к базе данных.

### Необходимы переменные окружения
`API_PORT` - порт, на котором запустится бэкенд

`API_DB_USER` - пользователь базы данных

`API_DB_PASSWORD` - пароль пользователя базы данных

`API_DB_HOST` - хост базы данных

`API_DB_PORT` - порт, на котором запустится база данных

`API_DB_NAME` - название базы данных

`API_DB_USE_SSL` - нужен ли сертификат ssl для доступа к базе данных

`API_DEBUG_MODE` - дебаг режим


### Как запускать

Для запуска бэкенда:
```commandline
python -m venv venv
./venv/bin/activate
pip install -r requirements.txt
python main.py
```

Для полной очистки базы данных:
```commandline
python -m venv venv
./venv/bin/activate
pip install -r requirements.txt
python init_db.py
```
