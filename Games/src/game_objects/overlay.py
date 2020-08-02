from src.game_objects.resources import GameObject
from src.helpers.helpers import round_vector
from src.configs.game_state import SCREEN_DIM
from src.configs.color_map import skytint
import pygame
from pygame import Color

class SkyTint(GameObject):
    def __init__(self, starting_hour=15):
        super().__init__(SCREEN_DIM, [0,0])
        self.image = pygame.Surface(round_vector(SCREEN_DIM), pygame.SRCALPHA)
        self.color_pallet = skytint
        self.target_color = Color([0,0,0,0])
        self.color = Color([0,0,0,0])

        for t in skytint.keys():
            if t <= starting_hour:
                self.time = t
            else:
                self.target_time = t
                break
        self.color.hsva = self.color_pallet[self.time]
        self.target_color.hsva = self.color_pallet[self.target_time]
        self.set_calc()

    def set_calc(self):
        if self.target_time > self.time:
            self.calc_hour = lambda x: (x - self.time) / (self.target_time - self.time)
        else:
            self.calc_hour = lambda x: (x - self.time) / (24+self.target_time - (self.time)) if x > self.time else (x + (24-self.time)) / (24+self.target_time - (self.time))

    def set_color(self, hour):
        if  0 > self.calc_hour(hour) or self.calc_hour(hour) > 1:
            self.time = self.target_time
            for h in range(1,25):
                self.target_time = int(hour) + h
                if self.target_time >= 24:
                    self.target_time -= 24
                if self.target_time in self.color_pallet:
                    break                
            self.color.hsva = self.color_pallet[self.time]
            self.target_color.hsva = self.color_pallet[self.target_time]
            self.set_calc()

        # print(self.color.hsva, self.target_color.hsva, hour, self.target_time, self.time, self.calc_hour(hour))
        self.hour = self.calc_hour(hour)
        
    def update(self):
        color = self.color.lerp(self.target_color, self.hour)
        self.image.fill(color)


