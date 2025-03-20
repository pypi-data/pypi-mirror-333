from app.settings import CELERY_TASK_INCLUDE
from infrastructure.celery.celery_app import create_celery_app
from infrastructure.celery.schema import CeleryConfig

celery_app = create_celery_app(celery_config=CeleryConfig(include=CELERY_TASK_INCLUDE))
