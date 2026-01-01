try:
    from celery import Celery
except ImportError:
    Celery = None

if Celery:
    celery_app = Celery(
        "cpos",
        broker="redis://localhost:6379/0",
        backend="redis://localhost:6379/0",
    )
else:
    celery_app = None
