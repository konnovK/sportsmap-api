# SportsMap API
![https://github.com/konnovK/sportsmap-api/actions/workflows/CI.yml](https://github.com/konnovK/sportsmap-api/workflows/CI/badge.svg)

Бэкенд для веб приложения с картой спортивных объектов СПб.

## SSL для базы данных

В корне проекта необходимо положить файл `CA.pem`, в котором
находится ssl сертификат для доступа к базе данных.

---
Подробнее о получении `CA.pem` файла:
- https://cloud.yandex.ru/docs/managed-postgresql/operations/connect#get-ssl-cert

## Необходимы переменные окружения

- `API_PORT` - порт, на котором запустится бэкенд
- `API_DB_USER` - пользователь базы данных
- `API_DB_PASSWORD` - пароль пользователя базы данных
- `API_DB_HOST` - хост базы данных
- `API_DB_PORT` - порт, на котором запустится база данных
- `API_DB_NAME` - название базы данных
- `API_DB_USE_SSL` - нужен ли сертификат ssl для доступа к базе данных
- `API_DEBUG_MODE` - дебаг режим

## Разработка

### Быстрые команды

- `make` Отобразить список доступных команд
- `make devenv` Создать и настроить виртуальное окружение для разработки
- `make lint` Запустить линтер
- `make test` Запустить тесты
- `make run` Запустить API локально

make использует переменные из файла `.env`.

### Также может пригодиться

Для полной очистки базы данных ~~пожалуйста не запускайте~~ используется скрипт `init_db.py`: 
```commandline
echo 'я прогаю уже 40 часов без еды и воды помогите'
python -m venv venv
./venv/bin/activate
pip install -r requirements.txt
python init_db.py
```
