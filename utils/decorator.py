import functools
import time

from system.log_helper import qlogger


def cost_time(func=None):
    def decorate(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            filename = fn.__code__.co_filename.split("\\")[-1][:-3]
            func_name = fn.__code__.co_name
            line_no = fn.__code__.co_firstlineno
            # print(f"{filename}:{func_name}:{line_no}: start")
            qlogger.info(f"{filename}:{func_name}:{line_no}: start")
            start_time = time.perf_counter()
            result = fn(*args, **kwargs)

            elapsed_time = time.perf_counter() - start_time
            # print(f"{filename}:{func_name}:{line_no}: cost: {elapsed_time}")
            qlogger.info(f"{filename}:{func_name}:{line_no}: cost: {elapsed_time}")

            return result

        return wrapper

    if func is None:
        return decorate
    return decorate(func)
