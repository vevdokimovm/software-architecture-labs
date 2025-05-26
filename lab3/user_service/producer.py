import pika
import json
import os

RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")

def publish_user_created(user_data: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    channel = connection.channel()

    channel.exchange_declare(exchange='user.created', exchange_type='fanout', durable=True)

    message = json.dumps(user_data)
    channel.basic_publish(exchange='user.created', routing_key='', body=message)

    print(f" [x] Sent event to exchange: {message}")
    connection.close()
