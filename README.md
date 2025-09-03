# Test QnA API

Простой Django REST Framework проект для вопросов и ответов с использованием PostgreSQL и Docker.

---

## Описание

Проект реализует API для создания, получения и удаления вопросов и ответов.  
Использует Django + DRF + PostgreSQL в Docker-контейнерах.

---

## Стек технологий

- Python 3.12
- Django 4.2
- Django REST Framework
- PostgreSQL 15
- Gunicorn
- Docker, Docker Compose

---

## Структура проекта

```
test_qna_api/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── app/
│   ├── init.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── questions/
│   ├── migrations/
│   ├── init.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
└── manage.py
```

---

## Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone https://github.com/D-Danis/test_qna_api_django.git
cd app
```

### 2. Запустить с Docker

> Для запуска проекта необходимы [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/).

```bash
docker-compose up --build
```

- Это соберёт образы, поднимет PostgreSQL и Django сервер.
- После успешного запуска сервер будет доступен по адресу: [http://localhost:8000](http://localhost:8000)
- Миграции будут применены автоматически при запуске.

### 3. Запуск тестов

Чтобы выполнить тесты, используйте команду:

```bash
docker-compose run web pytest -v
```

## Работа с API

### Маршруты

- `GET /questions/` — получить список вопросов
- `POST /questions/` — создать вопрос (требуется поле `text`)
- `DELETE /questions/{id}/` — удалить вопрос (удалит все ответы к нему)
- `POST /questions/{id}/answers/` — добавить ответ к вопросу (требуются `user_id` и `text`)
- `GET /answers/{id}/` — получить ответ по ID
- `DELETE /answers/{id}/` — удалить ответ

---

## Полезные команды Docker

▎Остановить контейнеры

```bash
docker-compose down
```

▎Просмотр логов приложения

```bash
docker-compose logs -f web
```

▎Выполнить миграции вручную (если надо)

```bash
docker-compose run web python manage.py migrate
```
