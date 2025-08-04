from celery import Celery
from datetime import timedelta
import os

# your_project_name/celery.py
# تنظیم متغیر محیطی برای جنگو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A.settings')

# ایجاد نمونه (instance) از Celery App

celery_app = Celery('A')

# پیدا کردن خودکار Taskها در فایل‌های tasks.py داخل appهای جنگو
# این باعث میشه نیازی نباشه تک تک Taskها رو import کنید
celery_app.autodiscover_tasks()


celery_app.conf.broker_url = 'amqp://rabbitmq'
celery_app.conf.result_backend = 'rpc://'
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'json'
celery_app.conf.accept_content = ['json',]
celery_app.conf.result_expires = timedelta(days=1)
celery_app.conf.task_always_eager = False
celery_app.conf.worker_prefetch_multiplire = 4