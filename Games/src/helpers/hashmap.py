
import json
import numpy as np
from src.helpers.helpers import load_json
import uuid
class Chunks:
    def __init__(self):
        self.filepath = 'src/assets/data/chunks.json'
        self.max_size = 1024
        self.load_chunks()

    def load_chunks(self):
        self.chunk_table = load_json(self.filepath)
        if self.chunk_table is None:
            print('File not found. Making new. Dont forget to change the chunk_size')
            self.chunk_table = self.make_chunk_table(4)
            self.save_chunks()
        pass

    def set_chunk_size(self, power):
        if type(power) != int:
            raise ValueError("Must be a int value")
        _chunk_size = 2**power
        if self.chunk_size != _chunk_size:
            self.chunk_size  = _chunk_size
            return self.chunk_size
        else: 
            return False

    def make_chunk_table(self, power=None):
        if power != None:
            self.set_chunk_size(power)
        array_size = round(self.max_size/self.chunk_size)
        chunk_table = np.array([str(uuid.uuid4()) for _ in range(array_size*array_size)])
        chunk_table = np.reshape(chunk_table, (array_size,array_size))
        return chunk_table

    def save_chunks(self):
        if self.filepath is None:
            raise ValueError('file path not set')
        self.table = {
            'chunkSize': self.chunk_size,
            'maxSize': self.max_size,
            'chunks': self.chunks.tolist(),
            'elements': self.elements
        }
        with open(self.file, 'w') as f:
            json.dump(self.table, f)
        print('chunks saved')


class HashTable:
    def __init__(self, filename='hashtable'):
        self.file = f'src/assets/data/{filename}.json'
        self.max_size = 1024
        self.elements = {}
        if filename is not None:
            self.load()

    def add_element(self, element, hash_id=None):
        '''
        Pega o chunk baseado na posição.
        é vazio? Cria lista, coloca o elemento, e enfia na tabela
        Não é? Append na lista
        '''
        print()
        x, y = self.chunk_point(element['position'])
        if not hash_id:
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
        for chunk in self.elements.values():
            if hash_id in chunk:
                chunk.pop(hash_id)
                return True
        return False
     
    def set_chunk_size(self, power):
        if type(power) != int:
            raise ValueError("Must be a int value")
        _chunk_size = 2**power
        if self.chunk_size != _chunk_size:
            self.chunk_size  = _chunk_size
            return self.chunk_size
        else: 
            return False

    def update_chunks(self, power):
        print('changing chunk size')
        if not self.set_chunk_size(power):
            return
        self.chunks = self.make_chunk_table(power)  

        for chunk, values in self.elements.copy().items():
            for hash_id, value in values.items():
                self.add_element(value, hash_id)
            self.elements.pop(chunk)
        self.save()  


    def make_chunk_table(self, power=None):
        if power != None:
            self.set_chunk_size(power)
        array_size = round(self.max_size/self.chunk_size)
        chunk_table = np.array([str(uuid.uuid4()) for _ in range(array_size*array_size)])
        chunk_table = np.reshape(chunk_table, (array_size,array_size))
        return chunk_table

    def save(self):

        if self.file is None:
            raise ValueError('file path not set')
        self.table = {
            'chunkSize': self.chunk_size,
            'maxSize': self.max_size,
            'chunks': self.chunks.tolist(),
            'elements': self.elements
        }
        with open(self.file, 'w') as f:
            json.dump(self.table, f)
        print('chunks saved')
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