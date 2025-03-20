CELERY_TASK_INCLUDE = [
    'app.celery.tasks',
    'core.tool.rpc.http.http_tool_async_celery'
]
'''配置celery扫描task的路径'''
