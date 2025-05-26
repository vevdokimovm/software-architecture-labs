# Лабораторная работа №3 — Event-driven архитектура и кэширование

## Цель работы

Реализовать архитектуру обмена событиями между двумя микросервисами с использованием брокера сообщений RabbitMQ, а также подключить in-memory кэш KeyDB.

## Стек технологий

- Python 3.10
- FastAPI
- PostgreSQL 15
- RabbitMQ + pika
- Redis (KeyDB)
- SQLAlchemy
- Docker / Docker Compose

## Структура

```text
lab3/ 
├── docker-compose.yaml 
├── .env 
├── user_service/ 
│ ├── main.py 
│ ├── models.py 
│ ├── db.py 
│ ├── cache.py 
│ ├── producer.py 
│ ├── requirements.txt 
│ └── Dockerfile 
├── notification_service/ 
│ ├── consumer.py 
│ ├── requirements.txt 
│ └── Dockerfile
```

## Архитектура

1. `user_service` создаёт пользователя и публикует событие `user.created` в exchange.
2. `notification_service` подписан на очередь, привязанную к `fanout` exchange, и выводит уведомление.
3. Данные пользователей кэшируются через KeyDB.

## Запуск

```bash
docker compose up --build
