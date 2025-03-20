from celery import Celery

app = Celery('celery_app', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')


# 定义一个普通函数
def add(x, y):
    return x + y

# 在运行时动态注册任务
_add = app.task(add, name='celery_app.add')

# 调用任务
result = _add.delay(4, 5)
print(f"Task result: {result.get()}")
