import pygame
from pygame import Vector3, Vector2
from helpers import round_vector

class InteractiveScreen:
    def __init__(self, title="Default"):
                
        pygame.init()
        pygame.font.init()

        self.SCREEN_DIM = Vector2(500,500)
        self.title = title
        self.screen = pygame.display.set_mode(round_vector(self.SCREEN_DIM))
        self.clock = pygame.time.Clock()
        self.toggle_run =True
        self.elements = []
        pygame.display.set_caption(self.title)

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.toggle_run = False
            if event.type == pygame.KEYDOWN:
                pass
            if event.type == pygame.KEYUP:
                pass
        out=0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            out = -1
        if keys[pygame.K_e]:
            out =  1

        self.screen.fill((0,0,0))
        for element in self.elements:
            if isinstance(element, Rectangle):
                pygame.draw.rect(self.screen, element.color, element.shape)
            else:
                continue
                self.screen.blit(element)
        pygame.display.update()
        # print("Tick")
        self.clock.tick(60)
        return out

class Rectangle:
    def __init__(self,position, size, color):
        self.shape = pygame.Rect(position, size)
        self.color = color
