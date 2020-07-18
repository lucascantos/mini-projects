
import numpy as np
import math
from matplotlib import pyplot as plt
class PerlinNoise:
    def __init__(self, shape, res, offset=[0,0], seed=None):
        self.shape = shape
        self.res = res
        self.offset = offset
        self.seed = None
        self.generate_perlin_noise_2d()
    
    def get_noise(self):
        return self._noise 

    def generate_perlin_noise_2d(self):  
        def f(t):
            return 6*t**5 - 15*t**4 + 10*t**3 
            
        def random_array():
            from random import random, seed
            for x in np.linspace(0,self.res[0]+1,self.res[0]+1):
                for y in np.linspace(0,self.res[1]+1,self.res[1]+1):
                    print(x)
                    s = (self.res[0]+1)*(x+self.offset[0])+(y+self.offset[1])
                    seed(s)
                    yield random()         

        delta = (self.res[0] / self.shape[0], self.res[1] / self.shape[1])
        d = (self.shape[0] // self.res[0], self.shape[1] // self.res[1])
        grid = np.mgrid[0:self.res[0]:delta[0],0:self.res[1]:delta[1]].transpose(1, 2, 0) % 1
      
        # Gradients
        if self.seed:
            np.random.seed(self.seed)    
            random_numbers = np.rand((self.res[0]+1, self.res[1]+1))
        else:                
            random_numbers = list(random_array())
            random_numbers = np.reshape(random_numbers, (self.res[0]+1, self.res[1]+1))
            print(random_numbers)
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
        self._noise = np.sqrt(2)*((1-t[:,:,1])*n0 + t[:,:,1]*n1)

    noise = property(get_noise, generate_perlin_noise_2d)

    def fractal(self, octaves=1, persistence=0.5):
        noise = np.zeros(self.shape)
        frequency = 1
        amplitude = 1
        for _ in range(octaves):
            noise += amplitude * self.noise
            frequency *= 2
            amplitude *= persistence
        return noise

    def normalized(self):
        x_min = np.amin(self.noise)
        x_max = np.amax(self.noise)
        return (self.noise - x_min)/(x_max-x_min)

def sinoid(x,f):
    return (2.0*(1-math.cos(x*3.1415/(f))))


if __name__ == "__main__":
    from configs.perlin_map import size, res, octave, p
    from simple_screen import InteractiveScreen, Rectangle
    from pygame import Vector2, Vector3
    from decorators import timeit
    res = 2
    offset = 0
    size = 64
    s = 4
    
    perlin = PerlinNoise([size,size], [res,res])
    pln = perlin.normalized()

    new_screen = InteractiveScreen()
    while new_screen.toggle_run:
        elements = []
        for x in range(size):
            for y in range(size):
                color = pln[x][y] * Vector3(255,255,255)
                elements.append(Rectangle(Vector2(x,y)*s, Vector2(1,1)*s, color))
        new_screen.elements = elements
        output = new_screen.run()
        if output:
            offset += output/2
            perlin.offset = [offset, 0]
            perlin.generate_perlin_noise_2d()
            pln = perlin.normalized()