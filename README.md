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
- Make
- Python версии 3.10 или выше

### Быстрые команды

**Makefile**, расположенный в `./api`:

- `make devenv` Создать и настроить виртуальное окружение для разработки
- `make postgres` Создать docker контейнеры с базами данных для тестов и разработки
- `make migrate` Применить миграции на базы данных для тестов и разработки
- `make migrations` Создать миграции
- `make lint` Запустить линтер [pylama](https://pypi.org/project/pylama/)
- `make test` Запустить тесты [pytest](https://pypi.org/project/pytest/)
- `make run` Запустить API локально

### Как подготовить окружение к разработке

```commandline
make devenv
make postgres
make migrate
```

В результате в текущей директории создастся виртуальное окружение python, 
в docker поднимется база данных postgres для тестов и для разработки,
и к этим базам применятся миграции

### Как запустить тесты

```commandline
make devenv
make postgres
make test
```

В результате сработает линтер и прогонятся тесты

### Как запустить API локально

```commandline
make devenv
make postgres
make migrate
make run
```

## Деплой

API разворачивается в виде docker контрейнера, в registry 
от yandex.cloud. Настроен экшн, который делает это автоматически при пуше в мейн.
Также этот экшн накатывает миграции на БД.

Следует обратить внимание на секреты для экшнов:

- `REGISTRY_ID` - id registry от yandex.cloud
- `OAUTH` - токен аутентификации для registry от yandex.cloud
- `DB_URL` - URL базы данных в проде
