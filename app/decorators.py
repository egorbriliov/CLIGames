import os
import time


def cls_clear(time_to_sleep):
    """
    Очищает консоль через некоторое время
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            time.sleep(time_to_sleep)
            os.system('cls||clear')
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator