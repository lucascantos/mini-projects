import pygame
from pygame import Vector3, Vector2
from src.helpers.helpers import round_vector

class InteractiveScreen:
    def __init__(self, title="Default"):
                
        pygame.init()
        pygame.font.init()

        self.SCREEN_DIM = Vector2(500,500)
        self.title = title
        self.screen = pygame.display.set_mode(round_vector(self.SCREEN_DIM))
        self.clock = pygame.time.Clock()
        self.toggle_run =True
        pygame.display.set_caption(self.title)
    
    def render(self, elements):
        self.screen.fill((0,0,0))
        all_sprites = pygame.sprite.RenderPlain(elements)
        all_sprites.draw(self.screen)
        # for element in elements:
        #     if isinstance(element, Rectangle):
        #         pygame.draw.rect(self.screen, element.color, element.shape)
        #     else:
        #         continue
        #         self.screen.blit(element)

    def run(self):
        
        # Input

        # Update

        # Render 

        pygame.display.update()
        self.clock.tick(60)

class Rectangle:
    def __init__(self,position, size, color):
        self.shape = pygame.Rect(position, size)
        self.color = color
