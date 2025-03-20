from celery import Celery
from celery.signals import task_postrun

app = Celery('my_app', broker='redis://localhost:6379/5', result_backend='redis://localhost:6379/6')

@app.task(name='my_app.add')
def add(x, y):
    return x + y

@task_postrun.connect
def my_postrun_handler(sender, task_id, task, args, kwargs, retval, state, **extra):
    print(f"xxxxxxxx Task {task_id} finished with result: {retval}")

# 调用任务
print('task add')
result = add.apply_async(args=[4, 4])


# print(f"Task result: {result.get(timeout=10)}")

# ../../.venv/bin/celery -A test_celery_callback:app worker --loglevel=debug
