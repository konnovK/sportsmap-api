# SportsMap API

Бэкенд для веб приложения с картой спортивных объектов СПб. Приложение разворачивается в яндекс.облаке,
с помощью **docker** и **docker compose**.

### Приложению необходимы переменные окружения

- `API_HOST` - хост, на котором запускается бэкенд
- `API_PORT` - порт, на котором запустится бэкенд
- `API_DB_URL` - адрес базы данных
- `API_DB_USE_SSL` - нужен ли сертификат ssl для доступа к базе данных

### SSL для базы данных

В корне проекта необходимо положить файл `CA.pem`, в котором
находится ssl сертификат для доступа к базе данных (если для подключения к базе это требуется).

Подробнее о получении `CA.pem` файла:
- https://cloud.yandex.ru/docs/managed-postgresql/operations/connect#get-ssl-cert

## Разработка

### Требования

- Docker
- Python версии 3.10 или выше

## Деплой

API разворачивается в виде docker контрейнера, в registry 
от yandex.cloud. Настроен экшн, который делает это автоматически при пуше в мейн.
Также этот экшн накатывает миграции на БД.

Следует обратить внимание на секреты для экшнов:

- `REGISTRY_ID` - id registry от yandex.cloud
- `OAUTH` - токен аутентификации для registry от yandex.cloud
- `DB_URL` - URL базы данных в проде
