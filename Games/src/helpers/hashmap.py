
import json
import numpy as np
from src.helpers.helpers import load_json, save_json
import uuid
from src.helpers.decorators import timeit
class Chunks:
    def __init__(self):
        self.chunksfile = 'src/assets/data/chunks.json'
        self.max_size = 1024
        self.chunk_size=1
        self.load()
        
    def load(self):
        hashtable = load_json(self.chunksfile)
        if hashtable is None:
            print('File not found. Making new. Dont forget to change the chunk_size')
            hashtable = self.make_chunk_table(2)
            return hashtable
        self.chunk_size = hashtable['chunkSize']
        self.max_size = hashtable['maxSize']
        array_size = round(self.max_size/self.chunk_size)
        self.chunks = np.array(hashtable['chunks']).reshape(array_size,array_size)

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
        self.chunks = np.array([str(uuid.uuid4()) for _ in range(array_size*array_size)])
        self.chunks = np.reshape(self.chunks, (array_size,array_size))
        self.save_chunks()
        return self.chunks

    def save_chunks(self):
        if self.chunksfile is None:
            raise ValueError('file path not set')
        table = {
            'chunkSize': self.chunk_size,
            'maxSize': self.max_size,
            'chunks': self.chunks.tolist()
        }
        with open(self.chunksfile, 'w') as f:
            json.dump(table, f)
        print('chunks saved')

class HashTable(Chunks):
    def __init__(self, filename='hashtable'):
        super().__init__()
        self.filepath = f'src/assets/data/{filename}.json'
        if filename is not None:
            self.elements = load_json(self.filepath)
            if self.elements is None:
                self.elements = {}

    def add_element(self, element, hash_id=None):
        '''
        Pega o chunk baseado na posição.
        é vazio? Cria lista, coloca o elemento, e enfia na tabela
        Não é? Append na lista
        '''
        x, y = self.chunk_point(element['position'])
        if not hash_id:
            hash_id = str(uuid.uuid4())
        if self.chunks[x][y] in self.elements:
            self.elements[self.chunks[x][y]][hash_id] = element
        else:
            self.elements[self.chunks[x][y]] = {hash_id: element}
        return hash_id

    def remove_element(self, hash_id):
        for chunk in self.elements.values():
            if hash_id in chunk:
                chunk.pop(hash_id)
                return True
        return False

    def chunk_point(self,coords):
        return [int(coord / self.chunk_size) for coord in coords]

    def subchunk_point(self,coords):
        return [round(coord / self.chunk_size) for coord in coords]
     
    def update_chunks(self):
        for chunk, values in self.elements.copy().items():
            for hash_id, value in values.items():
                self.add_element(value, hash_id)
            self.elements.pop(chunk)
        self.save()

    def save(self):
        save_json(self.elements, self.filepath)

    def inside_check(self, point, bbox):
        if bbox[0] <= point[0] < bbox[2] and bbox[1] <= point[1] < bbox[3]:
            return True
        else:
            return False