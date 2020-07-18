
import numpy as np
import math
from matplotlib import pyplot as plt
from decorators import timeit
class PerlinNoise:
    def __init__(self, shape, res_pwr, value=0, offset=[0,0]):
        self.shape = shape
        self.res_pwr = res_pwr
        self.offset = offset
        self.value = value

        self.set_resolution()
        self.set_zoom()
        self.set_noise()
        

    def get_resolution(self):
        return self._res        
    def set_resolution(self):
        self._res = [2**self.res_pwr + 1,  2**self.res_pwr + 1]
    res = property(get_resolution, set_resolution)

    def get_zoom(self):
        return self._zoom
    def set_zoom(self):
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
            for x in range(self.zoom+1):
                for y in range(self.zoom+1):
                    s = (2**self.res_pwr)*(x+self.offset[0])+(y+self.offset[1])
                    random.seed(s)
                    yield random.random()      


        delta = (self.zoom / self.shape[0], self.zoom / self.shape[1])
        d = (self.shape[0] // self.zoom, self.shape[1] // self.zoom)
        grid = np.mgrid[0:self.zoom:delta[0],0:self.zoom:delta[1]].transpose(1, 2, 0) % 1
    
        # Gradients
        # if seed:
        #     np.random.seed(seed)    
        #     random_numbers = np.random.rand(self.zoom+1, self.zoom+1)
        # else:                
        random_numbers = list(random_array())
        random_numbers = np.reshape(random_numbers, (1+self.zoom, 1+self.zoom))
        
        print(random_numbers.shape)
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


    def fractal(self, octaves=1, persistence=0.5,seed=10):
        noise = np.zeros(self.shape)
        frequency = 1
        amplitude = 1
        for _ in range(octaves):
            print (amplitude)
            frequency *= 2
            self.value -=1
            self.set_zoom()
            print(self.zoom)
            amplitude *= persistence
            noise += amplitude * self.generate_perlin_noise_2d()
        return noise+self.noise

    def normalized(self, array=None):
        if array is None:
            array = self.noise
        x_min = np.amin(array)
        x_max = np.amax(array)
        return (array - x_min)/(x_max-x_min)

    def sinoid(self,x,f):
        return (2.0*(1-math.cos(x*3.1415/(f))))
