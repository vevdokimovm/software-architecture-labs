from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

# Читаем переменные окружения
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")

# Подключение к БД
def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
    )

# Создание таблицы, если её нет
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# Вызываем функцию создания таблицы перед запуском сервера
create_table()

@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users;")
    users = [{"id": row[0], "name": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("APP_PORT", 8080)))