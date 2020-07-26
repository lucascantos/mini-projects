
import numpy as np
import math
from matplotlib import pyplot as plt
import json
# from src.helpers.decorators import timeit
class PerlinNoise:
    def __init__(self, size, res_pwr, zoom_value=0, offset=[0,0], seed=None):
        self.size = size
        self.res_pwr = res_pwr
        self.offset = offset
        if zoom_value != 0:
            self.zoom = zoom_value
        else:
            self.zoom = self.res_pwr-1

        self.set_resolution()
        

    def get_resolution(self):
        return self._res        
    def set_resolution(self):
        self._res = [2**self.res_pwr + 1,  2**self.res_pwr + 1]
    res = property(get_resolution, set_resolution)

    def get_zoom(self):
        return self._zoom
    def set_zoom(self, value):
        self.value = value
        self._zoom = 2**(self.res_pwr-self.value)
    zoom = property(get_zoom, set_zoom)

    def get_noise(self):
        return self._noise
    def set_noise(self):
        self._noise = self.generate_perlin_noise_2d()

    noise = property(get_noise, set_noise)

    def generate_perlin_noise_2d(self):  
        def f(t):
            return 6*t**5 - 15*t**4 + 10*t**3 
            
        def random_array():
            import random
            step = self.zoom+1
            full_range = [
                np.linspace(self.offset[0]-(self.zoom/2), self.offset[0]+(self.zoom/2), step),
                np.linspace(self.offset[1]-(self.zoom/2), self.offset[1]+(self.zoom/2), step)
            ]
            for x in full_range[0]:
                for y in full_range[1]:
                    s = (2**self.res_pwr)*(x+self.offset[0])+(y+self.offset[1])
                    random.seed(s)
                    yield round(random.random(),1)

        zoom = self.zoom

        delta = (zoom / self.size, zoom / self.size)
        d = (self.size // zoom, self.size // zoom)
        grid = np.mgrid[0:zoom:delta[0],0:zoom:delta[1]].transpose(1, 2, 0) % 1
    
        # Gradients
        # if seed:
        #     np.random.seed(seed)    
        #     random_numbers = np.random.rand(self.zoom+1, self.zoom+1)
        # else:                
        random_numbers = list(random_array())
        
        random_numbers = np.reshape(random_numbers, (zoom+1, zoom+1))
        
        # print(random_numbers.shape)
        angles = 2*np.pi*random_numbers
        gradients = np.dstack((np.cos(angles), np.sin(angles)))
        g00 = gradients[0:-1,0:-1].repeat(d[0], 0).repeat(d[1], 1)
        g10 = gradients[1:,0:-1].repeat(d[0], 0).repeat(d[1], 1)
        g01 = gradients[0:-1,1:].repeat(d[0], 0).repeat(d[1], 1)
        g11 = gradients[1:,1:].repeat(d[0], 0).repeat(d[1], 1)

        # Ramps
        n00 = np.sum(grid * g00, 2)
        n10 = np.sum(np.dstack((grid[:,:,0]-1, grid[:,:,1])) * g10, 2)
        n01 = np.sum(np.dstack((grid[:,:,0], grid[:,:,1]-1)) * g01, 2)
        n11 = np.sum(np.dstack((grid[:,:,0]-1, grid[:,:,1]-1)) * g11, 2)

        # Interpolation
        t = f(grid)
        n0 = n00*(1-t[:,:,0]) + t[:,:,0]*n10
        n1 = n01*(1-t[:,:,0]) + t[:,:,0]*n11
        return np.sqrt(2)*((1-t[:,:,1])*n0 + t[:,:,1]*n1)

    # @timeit
    def fractal(self, octaves=1, persistence=0.5):
        noise = np.zeros([self.size, self.size])
        frequency = 1
        amplitude = 1
        for _ in range(octaves):
            noise += amplitude * self.generate_perlin_noise_2d()
            frequency *= 2
            self.zoom = self.value - 1
            amplitude *= persistence
        self.zoom = self.value + octaves
        return noise

    def normalized (self, array=None):
        if array is None:
            array = self.noise
        x_min = np.amin(array)
        x_max = np.amax(array)
        return (array - x_min)/(x_max-x_min)

    def squared(self, array=None):
        if array is None:
            array = self.noise
        return np.sqrt(array * array)

    def sigmoid(self, threshold = 12, smooth = 1):
        f = self.size/2
        # bell = lambda x: 2.0*(1-math.cos(x*3.1415/(f))) if self.size*1/8 >= x or x >= self.size*7/8 else 1
        def bell(x):
            if x <= self.size / 2:
                k = self.size * (1 / threshold)
                signal = 1
            elif x >= self.size / 2:
                k = self.size*(1-1/threshold)
                signal = -1
            a = smooth
            a *= signal
            return round(1/(1+math.exp(-a*x + a* k)),2)
        
        continuous = np.linspace(0, self.size, self.size)
        a = list(map(bell, continuous))
        b = np.array(a).reshape((len(a), 1))
        c = np.array(a).reshape((1, len(a)))
        return self.normalized(b*c)



if __name__ == "__main__":
    from pygame import Vector2
    import matplotlib.pyplot as plt
    octave = 3
    max_res = 9
    size = 1024
    
    offset = Vector2(-4,-3.5)

    # Make Terrain
    perlin = PerlinNoise(size, max_res, seed=10)
    perlin.offset = offset
    perlin.zoom = 8
    pln = perlin.normalized(perlin.fractal(octave)) * perlin.sigmoid(threshold=8, smooth=0.04)
    print(pln.shape)


    # Make Resources

    perlin2 = PerlinNoise(size, 10, max_res-3)

    def resources(perlin_map, value, chance, weighted=False, weight_pwr=4):
        '''
        value = perlin value
        chance = resource density
        '''

        def tree_point(x):
            c = chance
            pwr = weight_pwr
            if weighted:
                c *=  2*x**pwr
            import random
            if x >= value:
                random.seed(x)
                if random.random() <= c:
                    return 1
            return 0
            
        return np.vectorize(tree_point)(perlin_map)
    
    pln2 = perlin2.normalized(perlin2.fractal())
    trees = resources(pln2, 0.6, 0.1, True) 
    x = trees[(pln >= 0.4) & (trees == 1)]
    trees = np.where((pln >= 0.4) & (trees == 1))

    perlin2.zoom = 4
    pln3 = perlin2.normalized(perlin2.fractal())
    rocks = resources(pln3, 0.6, 0.006) 
    rocks = np.where((pln >= 0.8) & (rocks == 1))
    

    x, y = trees
    fig, ax = plt.subplots()

    ax.imshow(pln)
    ax.scatter(y,x,c='k', s=0.1)    
    plt.show()

    import uuid
    print(uuid.uuid4())
    
    awe = {
        'type': 'terrain',
        'coords': [-44,-23],
        'properties':{
            'height': 0.5,
            'baseTemp': 295,
            'spawn': {
                'gameObject': 'tree',
                'id': 'string_id',
                'cooldown': 0, # Is available
                'offset': [-.5, 0.4] # Trying to avoid grid-like objects
            }
        }
    }
    
'''
    hash_table = {
        'power': 4
        'hash_id_chunk': {   
            'bbox': [0,0,31,31],
            'hash_id_grid': {
                'type': 'terrain',
                'coords': [-44,-23],
                'properties':{
                    'height': 0.5,
                    'baseTemp': 295,
                    'spawn': {
                        'gameObject': 'tree',
                        'id': 'string_id',
                        'cooldown': 0, # Is available
                        'offset': [-.5, 0.4] # Trying to avoid grid-like objects
                    }
                }
            },

            'hash_id_grid2': {
                'coords': [-45,-23],
                'type': 'character',
                'properties':{
                    'id': 'string_id'
                }
            },
        }       
    }
'''