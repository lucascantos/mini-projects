from src.functions.noise_generator import main as mapgen
from src.helpers.hashmap import Chunks, HashTable
from src.configs.animations import tileset
from uuid import uuid4
import random
import json
import numpy as np

def terrain_template (element):
    return {
        'type': str(type(element).__name__).lower(),
        'position': list(element.position),
        'properties':{
            'height': element.height,
            'baseTemp': 295,
            # 'spawn': element # Maybe add spawnable locations here
        }
    }

def make_data():
    height, trees, rocks = mapgen()
    def save(key, value):
        with open(f'src/assets/data/raw/{key}_map.json','w') as f:
            json.dump(values.tolist(), f)    
    for key, values in {'height': height, 'trees': trees, 'rocks': rocks}.items():
        save(key,value)
    return height, trees, rocks 

def make_files():

    keys = ['height', 'trees', 'rocks']
    def load(key):
        with open(f'src/assets/data/raw/{key}_map.json') as f:
            return np.array(json.load(f))

    resources = HashTable('resources')
    # hastable.change_chunk(4)

    data = {}
    for key in keys:
        data[key] = load(key)

    data['rocks'] = np.where((data['height'] >= 0.8) & (data['rocks'] == 1))
    data['trees'] = np.where((data['height'] >= 0.4) & (data['trees'] == 1))

    all_resources = {}

    y, x = data['trees']
    print(len(x), 'trees')
    for coords in zip(y.tolist(),x.tolist()):
        new_tree = {
            'type': 'tree',
            'position': coords,
            'offset': [round(random.random(),2), round(random.random(),2)]
        }
        hash_id = resources.add_element(new_tree)
        all_resources[hash_id] = new_tree

    y, x = data['rocks']
    print(len(x), 'rocks')
    for coords in zip(y.tolist(),x.tolist()):
        new_tree = {
            'type': 'rock',
            'position': coords,
            'offset': [round(random.random(),2), round(random.random(),2)]
        }
        hash_id = resources.add_element(new_tree)
        all_resources[hash_id] = new_tree
    print(len(all_resources))

    resources.save()

    from src.helpers.helpers import multi_threading

    bg_terrain = HashTable('terrain')
    def add_terrain(value):
        coords = value[0]
        height = value[1]
        if height <= 0.3:
            terrain = 'water'
        else:
            terrain = 'land'
        new_tree = {
            'type': terrain,
            'position': coords,
        }
        hash_id = bg_terrain.add_element(new_tree)
        all_resources[hash_id] = new_tree
        return coords

    for _ in multi_threading(add_terrain, np.ndenumerate(data['height'])):
        pass

    bg_terrain.save()

def update_chunks():
    chunks = Chunks()
    chunks.make_chunk_table(2)
    
    keys = ['resources', 'terrain']
    for key in keys:
        resources = HashTable(key)
        resources.update_chunks()
if __name__ == "__main__":
    # make_files()
    update_chunks()
    