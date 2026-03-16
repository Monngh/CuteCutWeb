import os
from celery import Celery

# Redis configuration, default to local if not set
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

# Render sometimes passes redis URIs that Celery dislikes.
# If it's a secure connection, we must explicitly tell Celery not to enforce strict SSL certs.
broker_settings = {}
if REDIS_URL and REDIS_URL.startswith("rediss://"):
    broker_settings["broker_use_ssl"] = {
        "ssl_cert_reqs": "none"
    }
    broker_settings["redis_backend_use_ssl"] = {
        "ssl_cert_reqs": "none"
    }

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
    **broker_settings
)
