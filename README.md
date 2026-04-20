# software-architecture-labs

Lab work for the **Software Architecture** course. Each lab explores a different architectural pattern using Python, Docker, and modern backend technologies.

## Labs Overview

| Lab | Topic | Stack |
|-----|-------|-------|
| [Lab 1](./lab1) | Containerization | Flask, PostgreSQL, Docker Compose |
| [Lab 2](./lab2) | REST API + DB | FastAPI, PostgreSQL, Docker Compose |
| [Lab 3](./lab3) | Event-driven architecture & caching | FastAPI, RabbitMQ, Redis/KeyDB, PostgreSQL |
| [Lab 4](./lab4) | Monitoring & alerting | FastAPI, Prometheus, Alertmanager |
| [Lab 5](./lab5) | Event Sourcing & CQRS | FastAPI, SQLite, Event Store |

## Tech Stack

- Python 3.10+
- FastAPI / Flask
- PostgreSQL
- RabbitMQ + pika
- Redis / KeyDB
- Prometheus + Alertmanager
- Docker & Docker Compose
- SQLAlchemy

## Running any lab

```bash
cd labN
cp .env.example .env   # fill in your values
docker compose up --build
```

## License

MIT
