import time

def execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Call the function
        end = time.time()  # Record the end time
        duration = end - start  # Calculate the duration
        print(f"The function '{func.__name__}' took {duration:.4f} seconds to execute.")
        return result
    return wrapper
