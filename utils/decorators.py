import time
from functools import wraps
from utils.logger import logger


def log_function_call(func):
    """记录函数调用日志"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            logger.info(f"{func.__name__} completed in {elapsed:.2f} seconds")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"{func.__name__} failed in {elapsed:.2f} seconds: {e}")
            raise
    return wrapper


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(delay * (2 ** attempt))
            logger.error(f"All {max_retries} attempts failed")
            raise last_exception
        return wrapper
    return decorator


def async_log_function_call(func):
    """异步函数调用日志"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        logger.info(f"Calling async {func.__name__} with args={args}, kwargs={kwargs}")
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            elapsed = time.time() - start_time
            logger.info(f"Async {func.__name__} completed in {elapsed:.2f} seconds")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"Async {func.__name__} failed in {elapsed:.2f} seconds: {e}")
            raise
    return wrapper
