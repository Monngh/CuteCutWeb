import os
from celery import Celery

# Redis configuration, default to local if not set
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

# Render sometimes passes redis URIs that Celery dislikes.
if REDIS_URL and REDIS_URL.startswith("rediss://"):
    # Celery prefers standard redis:// format unless SSL is explicitly configured with certs
    REDIS_URL = REDIS_URL.replace("rediss://", "redis://")
elif REDIS_URL and not REDIS_URL.startswith("redis"):
    REDIS_URL = f"redis://{REDIS_URL}"

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.worker.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
