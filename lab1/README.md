# Лабораторная №1 — Контейнеризация

## Цель
Упаковать Flask-приложение и PostgreSQL в Docker-контейнеры, настроить их взаимодействие через `docker-compose`.

## Компоненты
- Flask-приложение (port 8080)
- PostgreSQL (port 5432)
- Подключение через переменные окружения
- Конфигурация в `docker-compose.yaml`

## Запуск
```bash
docker compose up --build