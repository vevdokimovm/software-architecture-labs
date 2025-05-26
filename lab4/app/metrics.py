from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Latency of HTTP requests in seconds",
    ["endpoint"]
)
