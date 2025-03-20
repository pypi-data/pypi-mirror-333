"""
Time measurement for function call.
Developer: Dominik I. Braun
Contact: dome.braun@fau.de
Last Update: 2025-03-13
"""

import time
from functools import wraps


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(
            f"Function '{func.__name__}' took {elapsed_time:.3f} seconds to complete."
        )
        return result

    return wrapper
