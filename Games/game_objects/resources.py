import pygame
from pygame import Vector2
# from game_objects.character import Head
pygame.sprite.Sp
class GameObject(pygame.sprite.Sprite):
    def __init__(self, canvas_size, position):
        pygame.sprite.Sprite.__init__(self)
        self.position = Vector2()
        self.canvas = pygame.Surface(canvas_size) # Square to be draw uppon
        self.collision_box = None # Lista de masks
        self.graphic = None # Current frame to show
        self.animations = {
            'idle': {
                'frame': [1,2],
                'duration': [8,8]
            },
        }

    @property
    def center(self, obj=None):
        if obj is None:
            return Vector2(round(self.width/2), round(self.height/2))
        else:
            return Vector2(round(obj.getwidth()/2), round(obj.get_height()/2))
            
    @property
    def width(self):
        return self.canvas.get_width()
    @property
    def height(self):
        return self.canvas.get_height()

    def mask(self, shape):
        return pygame.mask.from_surface(shape)

    def move(self, offset):
        self.position += offset

class Resources(GameObject):
    pass

class Character(GameObject):
    def __init__(self, position):
        super().__init__(Vector2(32,32),position) 
        top_center = self.center
        top_center.y /= 2
        top_center -= self.canvas / 2

        bot_center = self.center
        bot_center.y *= 1.5
        bot_center -= self.canvas / 2

        self.collision_box = [
            self.mask(pygame.Rect(top_center,  self.canvas / 2 )),
            self.mask(pygame.Rect(bot_center,  self.canvas / 2 ))
        ]
        # self.head = Head()

class Player(Character):
    def __init__(self):
        super().__init__()
