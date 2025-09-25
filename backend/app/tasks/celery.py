from celery import Celery
from celery.signals import worker_process_init
from app.core.config import settings


celery_app = Celery("ai-post-scheduler")

@worker_process_init.connect
def init_worker(**kwargs):
    """Initialize worker process to avoid thread-local issues."""
    from celery.app.trace import reset_worker_optimizations
    reset_worker_optimizations()

celery_app.conf.update(
    broker_url=settings.CELERY_BROKER_URL,
    result_backend=settings.CELERY_RESULT_BACKEND,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    include=[
        'app.tasks.services.schedule_post',
    ],
    worker_prefetch_multiplier=1,
    # Periodic task configuration - runs every minute
    beat_schedule={
        'check-scheduled-posts': {
            'task': 'app.tasks.services.schedule_post.check_scheduled_posts',
            'schedule': 60.0,  # Run every 60 seconds (1 minute)
        },
    },
)