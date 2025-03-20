# type: ignore
"""装饰器工具类

提供重试机制、超时控制、性能计时、日志记录等功能。
"""

import time
import functools
import logging
import signal
from typing import Any, Callable, Dict, List, Optional, Type, Union
import threading

class DecoratorUtils:
    """装饰器工具类，提供各种装饰器的静态方法"""

    @staticmethod
    def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0,
              exceptions: Union[Type[Exception], tuple[Type[Exception], ...]] = Exception):
        """重试装饰器

        Args:
            max_attempts: 最大尝试次数，默认为3
            delay: 初始延迟时间（秒），默认为1.0
            backoff: 延迟时间的增长因子，默认为2.0
            exceptions: 需要捕获的异常类型，默认为Exception

        Returns:
            Callable: 装饰器函数

        Example:
            @DecoratorUtils.retry(max_attempts=5, delay=1, backoff=2, exceptions=(ConnectionError, TimeoutError))
            def fetch_data():
                # 可能失败的操作
                pass
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                mtries, mdelay = max_attempts, delay
                while mtries > 1:
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        msg = f"{func.__name__}: 第{max_attempts - mtries + 1}次尝试失败，{mdelay}秒后重试。错误: {str(e)}"
                        logging.warning(msg)
                        time.sleep(mdelay)
                        mtries -= 1
                        mdelay *= backoff
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def timeout(seconds: int):
        """超时装饰器（仅适用于Unix/Linux系统）

        Args:
            seconds: 超时时间（秒）

        Returns:
            Callable: 装饰器函数

        Raises:
            TimeoutError: 如果函数执行超时

        Example:
            @DecoratorUtils.timeout(5)
            def slow_function():
                time.sleep(10)
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                def handler(signum, frame):
                    raise TimeoutError(f"{func.__name__}执行超时（{seconds}秒）")

                # 设置信号处理器
                # type: ignore
                original_handler = signal.getsignal(signal.SIGALRM)
                # 在Windows系统中使用其他信号类型
                if hasattr(signal, 'SIGALRM'):
                    signal.signal(signal.SIGALRM, handler)
                else:
                    # Windows系统不支持SIGALRM，可以考虑使用threading.Timer作为替代方案
                    raise NotImplementedError("当前系统不支持SIGALRM信号")

                # 设置闹钟
                # 在Windows系统中使用其他定时方案
                if hasattr(signal, 'SIGALRM'):
                    signal.alarm(seconds)
                else:
                    timer = threading.Timer(seconds, lambda: handler(None, None))
                    timer.start()
                try:
                    result = func(*args, **kwargs)
                finally:
                    # 取消闹钟并恢复原始信号处理器
                    signal.alarm(0)
                    signal.signal(signal.SIGALRM, original_handler)
                return result
            return wrapper
        return decorator

    @staticmethod
    def timer(logger: Optional[logging.Logger] = None):
        """性能计时装饰器

        Args:
            logger: 日志记录器，如果为None则使用print输出

        Returns:
            Callable: 装饰器函数

        Example:
            @DecoratorUtils.timer()
            def process_data():
                # 耗时操作
                pass
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                elapsed = end_time - start_time
                msg = f"{func.__name__}执行耗时: {elapsed:.4f}秒"
                
                if logger:
                    logger.info(msg)
                else:
                    print(msg)
                return result
            return wrapper
        return decorator

    @staticmethod
    def log(logger: Optional[logging.Logger] = None, level: int = logging.INFO):
        """日志记录装饰器

        Args:
            logger: 日志记录器，如果为None则使用根日志记录器
            level: 日志级别，默认为INFO

        Returns:
            Callable: 装饰器函数

        Example:
            @DecoratorUtils.log(level=logging.DEBUG)
            def process_data(data):
                # 处理数据
                return result
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                func_logger = logger or logging.getLogger()
                func_args = ', '.join([repr(a) for a in args] + [f"{k}={repr(v)}" for k, v in kwargs.items()])
                func_logger.log(level, f"调用 {func.__name__}({func_args})")
                try:
                    result = func(*args, **kwargs)
                    func_logger.log(level, f"{func.__name__} 返回: {repr(result)}")
                    return result
                except Exception as e:
                    func_logger.exception(f"{func.__name__} 异常: {str(e)}")
                    raise
            return wrapper
        return decorator

    @staticmethod
    def cache(maxsize: int = 128):
        """简单缓存装饰器

        Args:
            maxsize: 最大缓存条目数，默认为128

        Returns:
            Callable: 装饰器函数

        Example:
            @DecoratorUtils.cache(maxsize=256)
            def fibonacci(n):
                if n <= 1:
                    return n
                return fibonacci(n-1) + fibonacci(n-2)
        """
        def decorator(func):
            cache_dict = {}
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # 创建可哈希的键
                key = str(args) + str(sorted(kwargs.items()))
                if key in cache_dict:
                    return cache_dict[key]
                
                result = func(*args, **kwargs)
                
                # 如果缓存已满，删除最早的条目
                if len(cache_dict) >= maxsize:
                    # 简单实现：直接清空缓存
                    # 更好的实现应该使用LRU策略
                    cache_dict.clear()
                    
                cache_dict[key] = result
                return result
            return wrapper
        return decorator