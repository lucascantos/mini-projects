
def round_vector(vector):
    return round(vector.x), round(vector.y)

def load_json(file):
    import json
    try:
        with open(file) as f:
            return json.load(f)
    except Exception as e:
        print("File not found")
        return None
        # raise ValueError(e)