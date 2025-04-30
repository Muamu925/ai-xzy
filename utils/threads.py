# -*- coding: utf-8 -*-
"""
utils/threads.py

后台线程管理工具，提供简化线程启动的函数。
"""
import threading

def start_thread(target, args=(), daemon=True):
    """
    启动一个后台线程执行 target 函数。
    """
    thread = threading.Thread(target=target, args=args)
    thread.daemon = daemon
    thread.start()
    return thread

def run_and_callback(target, args=(), callback=None, callback_args=()):
    """
    在后台线程执行 target，完成后调用 callback (在后台线程)。
    注意: 如果 callback 需要在主线程中更新UI，需要自行使用 tkinter 的 after 方法。
    """
    def wrapper():
        result = target(*args)
        if callback:
            callback(result, *callback_args)
    return start_thread(wrapper)
