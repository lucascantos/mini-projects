
def round_vector(vector):
    return round(vector.x), round(vector.y)

def load_json(file):
    import json
    try:
        with open(file) as f:
            return json.load(f)
    except:
        return None
        # raise ValueError(e)
    
def multi_threading(func, args):
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as executor:
        if func.__code__.co_argcount >= 2 :
            return executor.map(lambda args: func(**args), args)
        else:
            return executor.map(func, args)
