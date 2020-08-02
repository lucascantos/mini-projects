import pygame
from pygame import Vector3, Vector2
from src.helpers.helpers import round_vector

from src.helpers.decorators import timeit

class InteractiveScreen:
    def __init__(self, title="Default"):
        '''
        Main pygame screen to handle updates and blits
        :param title: str, Base title of screen
        '''
                
        pygame.init()
        pygame.font.init()

        self.SCREEN_DIM = Vector2(512,512)
        self.title = title
        self.screen = pygame.display.set_mode(round_vector(self.SCREEN_DIM))
        self.clock = pygame.time.Clock()
        self.toggle_run =True
        pygame.display.set_caption(self.title)
    
    @property
    def center(self):
        return round_vector(self.SCREEN_DIM/2)
        
    def get_all_sprites(self):
        return self._all_sprites

    def set_all_sprites(self, elements):
        self._all_sprites = pygame.sprite.RenderPlain(elements)

    all_sprites = property(get_all_sprites, set_all_sprites)

    def update(self):
        '''
        Run update to all sprites
        '''
        self.all_sprites.update()

    def render(self):
        '''
        Draw sprites and background
        '''
        self.screen.fill((0,0,0))
        self.all_sprites.draw(self.screen)


    def run(self):
        '''
        Update and render the elements
        '''
        
        pygame.display.set_caption(f'{self.title} - {str(int(self.clock.get_fps()))}fps')
        # Input

        # Update
        self.update()
        # Render 
        self.render()

        pygame.display.update()
        self.clock.tick(60)

class Rectangle:
    def __init__(self,position, size, color):
        self.shape = pygame.Rect(position, size)
        self.color = color
