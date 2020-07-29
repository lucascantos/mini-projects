
import json
import numpy as np
from src.helpers.helpers import load_json
import uuid

class HashTable:
    def __init__(self):
        self.file = 'src/assets/data/hashtable.json'
        self.max_size = 1024
        self.elements = {}
        self.load()

    def set_chunk_size(self, power):
        if type(power) != int:
            raise ValueError("Must be a int value")
        self.chunk_size = 2**power

    def add_element(self, element):
        '''
        Pega o chunk baseado na posição.
        é vazio? Cria lista, coloca o elemento, e enfia na tabela
        Não é? Append na lista
        '''

        x, y = self.chunk_point(element['position'])
        hash_id = str(uuid.uuid4())
        if self.chunks[x][y] in self.elements:
            self.elements[self.chunks[x][y]][hash_id] = element
        else:
            self.elements[self.chunks[x][y]] = {hash_id: element}
        return hash_id

    def chunk_point(self,coords):
        return [int(coord / self.chunk_size) for coord in coords]

    def subchunk_point(self,coords):
        return [round(coord / self.chunk_size) for coord in coords]

    def remove_element(self, hash_id):
        # if self.chunk_size is None:
        #     raise ValueError('chunk_size not defined')

        # for chunk in self.table.values():
        #     if hash_id in chunk:
        #         chunk.pop(hash_id)
        #         return True
        #     else:
        #         continue
        return False

    def change_chunk(self, power):
        new_table = self.make_chunk_table(power)

        # old_table = self.table.copy()        
        # self.table = {}
        
        # outbounds = []
        # old_table.pop('bbox')
        # for chunk in old_table.values():
        #     chunk.pop('bbox')
        #     for key in chunk.copy().keys():
        #         moving_element = chunk.pop(key)
        #         if not self.add_element(moving_element, key):
        #             outbounds.append(moving_element)
                  

    def make_chunk_table(self, power=None):
        if power != None:
            self.set_chunk_size(power)
        array_size = round(self.max_size/self.chunk_size)
        chunk_table = np.array([str(uuid.uuid4()) for _ in range(array_size*array_size)])
        chunk_table = np.reshape(chunk_table, (array_size,array_size))
        return chunk_table

    def save(self):
        self.table = {
            'chunkSize': self.chunk_size,
            'maxSize': self.max_size,
            'chunks': self.chunks.tolist(),
            'elements': self.elements
        }
        with open(self.file, 'w') as f:
            json.dump(self.table, f)

    def load(self):
        self.table = load_json(self.file)
        if self.table is None:
            print('File not found. Making new. Dont forget to change the chunk_size')
            self.set_chunk_size(4)
            self.chunks = self.make_chunk_table()
            self.save()
        self.max_size = self.table['maxSize']
        self.chunk_size = self.table['chunkSize']
        self.chunks = np.array(self.table['chunks'])
        self.elements = self.table['elements']
    
    def inside_check(self, point, bbox):
        if bbox[0] <= point[0] < bbox[2] and bbox[1] <= point[1] < bbox[3]:
            return True
        else:
            return False