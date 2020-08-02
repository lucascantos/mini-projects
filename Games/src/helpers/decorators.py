from time import time
def timeit(func):
    '''
    Mesure time of function
    '''
    def wrapper(*args, **kwargs):
        start = time()
        output = func(*args, **kwargs)
        print(f"Elapsed: {time()-start:.2f}s")
        return output  
    return wrapper
