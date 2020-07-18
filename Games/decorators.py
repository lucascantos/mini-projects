from time import time
def timeit(func):
    def wrapper(*args, **kwargs):
        start = time()
        output = func(*args, **kwargs)
        print(f"Elapsed: {time()-start}s")
        return output  
    return wrapper
