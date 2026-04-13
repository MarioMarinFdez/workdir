import time
from functools import wraps
from logger import get_logger

logger = get_logger(__name__)

def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        elapsed = round((end - start) * 1000, 2)
        logger.info(f"{func.__name__} ejecutado en {elapsed}ms")
        return result
    return wrapper
