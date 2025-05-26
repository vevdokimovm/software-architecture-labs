import pika
import os
import json
import time

RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
QUEUE_NAME = "user_notifications"

def callback(ch, method, properties, body):
    print("CALLBACK СРАБОТАЛ", flush=True)
    data = json.loads(body)
    print(f"Уведомление: создан пользователь {data['name']} ({data['email']})", flush=True)

def main():
    print("Подключились к RabbitMQ, подписываемся...", flush=True)
    # Подключаемся с повторными попытками
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
            break
        except pika.exceptions.AMQPConnectionError:
            print("Ждём подключения к RabbitMQ...", flush=True)
            time.sleep(2)

    channel = connection.channel()

    # Делаем именованный exchange и очередь
    channel.exchange_declare(exchange='user.created', exchange_type='fanout', durable=True)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.queue_bind(exchange='user.created', queue=QUEUE_NAME)

    print(' [*] Ожидаем события. Для выхода нажми CTRL+C', flush=True)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

if __name__ == "__main__":
    main()
