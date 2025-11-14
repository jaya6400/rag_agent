import os
from redis import Redis
from rq import Queue

redis_conn = Redis(
    host=os.getenv("REDIS_HOST", "valkey"),
    port=int(os.getenv("REDIS_PORT", 6379))
)

queue = Queue(connection=redis_conn)
