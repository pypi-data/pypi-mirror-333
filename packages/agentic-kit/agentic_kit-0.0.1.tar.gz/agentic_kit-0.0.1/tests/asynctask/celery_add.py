import os
import sys
import threading
from time import sleep

sys.path.append('/Users/manson/ai/app/agentic_kit/')

from tests.asynctask.celery_app import app

@app.task(name='celery_app.tasks.add')
def add(x, y):
    print(f"celery当前进程 ID: {os.getpid()}")
    print(f"celery当前线程 ID: {threading.get_ident()}")
    sleep(1)
    return x + y

# @task_success.connect(sender=add)
# def callback(sender=None, result=None, **kwargs):
#     print(f"callback当前进程 ID: {os.getpid()}")
#     print(f"callback当前线程 ID: {threading.get_ident()}")
#     print("Task succeeded! Result:", result)
#
#
# @task_failure.connect(sender=add)
# def callback(sender=None, result=None, **kwargs):
#     print(f"callback当前进程 ID: {os.getpid()}")
#     print(f"callback当前线程 ID: {threading.get_ident()}")
#     print("Task succeeded! Result:", result)