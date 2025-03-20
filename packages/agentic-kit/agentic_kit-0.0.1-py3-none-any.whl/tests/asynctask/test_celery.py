import asyncio
import os
import sys
import threading
import unittest
from time import sleep

import redis
from celery.signals import task_postrun, task_failure

from infrastructure.celery.celery_app import test_shared_task

sys.path.append('/Users/manson/ai/app/agentic_kit/')

from tests.asynctask.celery_add import add


def subscribe_redis():
    r = redis.Redis(host='localhost', port=6379, db=3)
    pubsub = r.pubsub()
    pubsub.subscribe("my_signal_channel")

    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Received notification: {message['data'].decode()}")
#
# r = redis.Redis(host='localhost', port=6379, db=3)
# pubsub = r.pubsub()
# pubsub.subscribe('my_signal_channel')
# for message in pubsub.listen():
#     if message['type'] == 'message':
#         print(f"Received message: {message['data'].decode()}")

#
# @task_postrun.connect
# def task_postrun_callback(sender=None, task_id=None, task=None, retval=None, **kwargs):
#     print('=====task_postrun_callback')
#     print(kwargs)
#     print(sender)
#     print(task)
#     print(retval)
#     print(f"Task {task_id} completed with result: {retval}")
#     import asyncio
#     asyncio.run(notify_task_completion(task_id, retval))
#
# @task_failure.connect
# def task_failure_callback(sender=None, task_id=None, exception=None, **kwargs):
#     print(f"Task {task_id} failed with exception: {exception}")


class MyTestCase(unittest.TestCase):
    def test_celery(self):
        print(f"main当前进程 ID: {os.getpid()}")
        print(f"main当前线程 ID: {threading.get_ident()}")
        # task = add.delay(2, 3)
        # test_shared_task.apply_async(kwargs={
        #     'text': 'nihao'
        # })
        text = 'aaaaaa'
        test_shared_task.apply_async(args=(text,))
        print(f"Task called")


        # result = task.get()
        # print(f"Task result: {result}")

        # subscribe_redis()

        # def on_message(body):
        #     print("Received result:", body['result'])

        # 启动任务并注册回调
        # result = add.delay(2, 3)
        # result.get(on_message=on_message)

        # print('sleep start')
        # sleep(10)
        # print('sleep end')


if __name__ == '__main__':
    unittest.main()
