from celery import Celery
from core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "autodirector",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.task_routes = {
    "workers.tasks.run_episode_graph": {"queue": "default"},
    "workers.tasks.upload_youtube": {"queue": "high"},
}

celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"
celery_app.conf.accept_content = ["json"]