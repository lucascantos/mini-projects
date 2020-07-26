
import json
from src.helpers.helpers import load_json
import uuid

class HashTable:
    def __init__(self):
        self.file = 'assets/data/hashtable.json'
        self.load()

    def add_element(self, element):
        if self.chunk_size is None:
            raise ValueError('chunk_size not defined')

        for chunk in self.table.values():
            if self.inside_check(element.position, chunk['bbox']):
                hash_id = element.pop('id')
                chunk[hash_id] = element
                return True
        return False

    def remove_element(self, hash_id):
        if self.chunk_size is None:
            raise ValueError('chunk_size not defined')

        for chunk in self.table.values():
            if hash_id in chunk:
                chunk.pop(hash_id)
                return True
            else:
                continue
        return False

    def change_chunk(self, power):
        self.chunk_size = 2 ** power
        max_size = 1024
        step = max_size/self.chunk_size
        old_table = self.table.copy()
        self.table = {}
        for x in range(0,max_size, step):
            for y in range(0,max_size, step):
                self.table[uuid.uuid4()] = {
                    'bbox': [x, y, x+step, y+step]
                }    
        
        outbounds = []
        for chunk in old_table.values():
            chunk.pop('bbox')
            for key in chunk.keys():
                moving_element = chunk.pop(key)
                if not self.add_element(moving_element):
                    outbounds.append(moving_element)
        print(len(outbounds))
                  
    def save(self):
        self.table['chunk_size'] = self.chunk_size
        with open(self.file, 'w') as f:
            json.dump(self.table, f)

    def load(self):
        self.table = load_json(self.file)
        self.chunk_size = self.table['chunk_size']
        if self.table is None:
            print('File not found. Making new. Dont forget to change the chunk_size')
            self.table = {}
            self.chunk_size = None
            self.save()

    def inside_check(self,point, bbox):
        if bbox[0] <= point.x < bbox[2] and bbox[1] <= point.y < bbox[3]:
            return True
        else:
            return False