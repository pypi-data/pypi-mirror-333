"""
Function logger (arguments and returns).
Developer: Dominik I. Braun
Contact: dome.braun@fau.de
Last Update: 2025-03-13
"""

from functools import wraps


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(
            f"Calling function {func.__name__} with \narguments: \n    {args}\n and kwargs: \n    {kwargs}"
        )
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned:\n    {result}")
        return result

    return wrapper
