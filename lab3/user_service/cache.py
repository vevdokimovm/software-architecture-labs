import redis
import os
import json

REDIS_HOST = os.getenv("REDIS_HOST", "keydb")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def get_user_from_cache(user_id: int):
    data = redis_client.get(f"user:{user_id}")
    if data:
        return json.loads(data)
    return None

def save_user_to_cache(user_id: int, user_data: dict):
    redis_client.set(f"user:{user_id}", json.dumps(user_data), ex=60)
