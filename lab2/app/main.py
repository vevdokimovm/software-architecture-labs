import redis
import psycopg2
import os
import flask import Flask, jsonify

app = Flask(__name__)

# Подключение к PostgreSQL
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")

def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
    )

# Создание таблицы, если её нет
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.executre("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

create_table()  # Автоматически создаёт таблицу при старте приложения

# Реализация Cache-Aside
@app.route("/users", methods=["GET"])
def get_users():
    cached_users = redis_client.get("users_cache")

    if cached_users:
        print("Данные взяты из кэша")
        return cached_users

    print("Данные загружены из БД")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users;")
    users = [{"id": row[0], "name": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()

    redis_client.setex("users_cache", 60, str(users))  # Кэшируем на 60 сек

    return jsonify(users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("APP_PORT", 8080)))