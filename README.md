# ServiceDesk

## Описание проекта

**ServiceDesk** — это система обработки обращений пользователей через электронную почту.  
Основные возможности проекта:
- Получение новых писем с электронной почты.
- Создание тикетов на основе писем.
- Отправка автоматических ответов пользователям.
- Ответы на тикеты через API с отправкой ответов пользователям по электронной почте.
- Изменение ответственного и статуса тикета.

## Стек технологий

- **Backend**: Python, FastAPI
- **Асинхронная работа с БД**: SQLAlchemy (Async)
- **Брокер задач**: Celery + Redis
- **ORM**: SQLAlchemy
- **База данных**: PostgreSQL
- **Тестирование**: pytest + HTTPX
- **Электронная почта**: smtplib + imaplib

## Как запустить проект

### Шаг 1. Клонируйте репозиторий
```bash
git clone https://github.com/a-yermakova/servicedesk.git
cd servicedesk
```
### Шаг 2. Установите зависимости
```bash
pip install poetry
poetry install
poetry shell
```
### Шаг 3. Настройте переменные окружения
Создайте файл .env в корневой директории проекта по шаблону:
```makefile
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
EMAIL_HOST=smtp.your-email-provider.com
EMAIL_PORT=993
EMAIL_USER=your-email@example.com
EMAIL_PASSWORD=your-email-password
SMTP_HOST=smtp.your-email-provider
SMTP_PORT=465
REDIS_HOST=localhost
REDIS_PORT=6379
```
### Шаг 4. Примените миграции базы данных
Для создания и обновления таблиц выполните:
```bash
alembic upgrade head
```
### Шаг 5. Запустите Celery Worker
```bash
celery -A app.celery_app.celery_app worker --loglevel=debug --concurrency 1 -P solo -Q email_queue
```
### Шаг 6. Запустите FastAPI
```bash
uvicorn app.main:app --reload
```
### Как запустить тесты
В корневой директории проекта выполните:
```bash
pytest
```