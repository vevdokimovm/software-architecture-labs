# Лабораторная №2 — Кэширование и Redis (KeyDB)

## Цель
Добавить кэширование с использованием KeyDB (Redis). Применить стратегию cache-aside.

## Компоненты
- KeyDB поднят в Docker
- keydb-cli: set, get, hash, list, set, zset, TTL
- Python: библиотека `redis`
- FastAPI endpoint `/users/{id}` использует кэширование

## Особенности
- `get_user_from_cache(user_id)`
- `save_user_to_cache(user_id, data)`
- TTL 60 секунд

## Проверка
1. Первый запрос: данные из БД
2. Повторный запрос: данные из Redis