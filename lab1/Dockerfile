# Используем официальный образ Python
FROM python:3.10

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта внутрь контейнера
COPY app/ /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Определяем переменную окружения для Flask
ENV FLASK_APP=/app/main.py

# Открываем порт 8080
EXPOSE 8080

# Запускаем приложение
CMD ["python", "/app/main.py"]
