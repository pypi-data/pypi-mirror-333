import time

from typing_extensions import Union

from app.celery.celery_app import celery_app
from infrastructure.event_driven.pub_sub.redis_publish import tool_call_publish_wrapper
from infrastructure.event_driven.pub_sub.redis_pubsub_manager import tool_call_publisher


@celery_app.task(name='celery_app.tasks.calculator_add')
@tool_call_publish_wrapper(publisher=tool_call_publisher)
def calculator_add(
    x: Union[int, float],
    y: Union[int, float],
    **kwargs
):
    print('=====celery_app.calculator_add=======')
    time.sleep(5)
    res = x + y
    print(f'calculator_add: {x} + {y} = {res}')
    print(kwargs)
    return    {
        'type': 'tool',
        'artifact': f'x + y = {res}',
        'content': res,
        'status': 'success',
        **kwargs
    }
