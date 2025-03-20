import os
import threading

import redis
from celery import Celery
from celery.signals import task_postrun

r = redis.Redis(host='localhost', port=6379, db=3)

def create_app():
    app = Celery('tasks', broker='redis://localhost:6379/0', include=[
            'celery_add'
        ])
    app.conf.update(
        result_backend='redis://localhost:6379/1',  # 用于存储任务结果
        accept_content=['json'],  # 接受的内容类型
        task_serializer='json',   # 任务序列化方式
        result_serializer='json', # 结果序列化方式
        timezone='UTC',           # 时区
        enable_utc=True,          # 使用 UTC 时间
    )

    return app


@task_postrun.connect(dispatch_uid='unique_callback')
def task_postrun_callback(sender=None, task_id=None, task=None, retval=None, **kwargs):
    print('=====task_postrun_callback')
    r.publish(f'my_signal_channel', f"Received signal from {task_id} with data: {retval}")

    print(f"callback当前进程 ID: {os.getpid()}")
    print(f"callback当前线程 ID: {threading.get_ident()}")
    print('kw : %s' % kwargs)
    print(f'sender = {sender}')
    print(f'task = {task}')
    print(f'retval = {retval}')
    print(f"Task {task_id} completed with result: {retval}")


app = create_app()

# ../../.venv/bin/celery -A celery_app:app worker --loglevel=debug
