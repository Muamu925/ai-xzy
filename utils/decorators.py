# -*- coding: utf-8 -*-
"""
utils/decorators.py

性能优化相关的装饰器，例如异步执行和计时。
"""
import threading
import time
import functools
import sys

def run_async(func):
    """
    装饰器：将函数放在独立线程中运行（不阻塞主线程）。
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
    return wrapper

def timing(func):
    """
    装饰器：计算函数执行时间并输出到控制台。
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"[TIMING] {func.__name__} 执行时间: {elapsed:.3f}秒", file=sys.stderr)
        return result
    return wrapper
