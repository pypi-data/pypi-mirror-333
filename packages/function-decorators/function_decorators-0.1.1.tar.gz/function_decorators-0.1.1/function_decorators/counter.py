from functools import wraps

# Global counter to track function calls
call_count = 0


def count_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global call_count
        call_count += 1  # Increment the call count every time the function is called
        print(f"Function '{func.__name__}' was called {call_count} times.")
        result = func(*args, **kwargs)
        return result

    return wrapper
