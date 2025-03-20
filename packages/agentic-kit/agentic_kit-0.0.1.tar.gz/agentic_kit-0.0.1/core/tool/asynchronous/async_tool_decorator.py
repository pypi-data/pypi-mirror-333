def set_tool_async(*args, **kwargs):
    def decorator(func):
        # for attr_name, value in kwargs.items():
        setattr(func, 'metadata', {'is_async': True})
        return func
    return decorator
