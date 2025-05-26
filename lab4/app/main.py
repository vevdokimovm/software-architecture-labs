from fastapi import FastAPI
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from metrics import REQUEST_COUNT, REQUEST_LATENCY
import time
import random

app = FastAPI()

@app.get("/")
def root():
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    start_time = time.time()
    time.sleep(random.uniform(0.1, 0.5))  # эмуляция задержки
    REQUEST_LATENCY.labels(endpoint="/").observe(time.time() - start_time)
    return {"message": "Hello from lab4"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
