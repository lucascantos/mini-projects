import pygame
from pygame import Vector2
# from game_objects.character import Head
class GameObject(pygame.sprite.Sprite):
    def __init__(self, canvas_size, position):
        pygame.sprite.Sprite.__init__(self)
        self.canvas = pygame.Rect(Vector2(), canvas_size) # Square to be draw uppon
        self.canvas.center = self.position
        self.collision_box = None # Lista de masks
        self.image = None # Current frame to show
        self.animations = {}

    @property
    def position(self):
            return self.canvas.center
            
    @property
    def width(self):
        return self.canvas.get_width()

    @property
    def height(self):
        return self.canvas.get_height()

    def make_animations(self, animation_info):
        output = {}
        if animation_info['type'] == 'sheet':
            get_image = lambda x: x
        elif animation_info['type'] == 'files':
            pass

        for name, value in animation_info.items():
            if value is None:
                
                output[name]: pygame.image.load(img_loc).convert()

class Resources(GameObject):
    pass

class Character(GameObject):
    def __init__(self, position):
        from animations import character
        super().__init__(Vector2(32,32),position) 
        top_center = self.canvas.center
        top_center.y /= 2
        top_center -= top_center / 2

        bot_center = self.canvas.center
        bot_center.y *= 1.5
        bot_center -= bot_center / 2

        self.collision_box = [
            pygame.Rect(top_center,  self.canvas / 2 ),
            pygame.Rect(bot_center,  self.canvas / 2 )
        ]
        # self.head = Head()

        self.animations = self.make_animations(character)



    def move(self, position):
        # check if bottom collision is true
        self.canvas.move_ip(position)

class Player(Character):
    def __init__(self):
        super().__init__()

'''

x_movement = Vector2(input_movement.x, 0)
if collision(player, element, x_movement):
    player_movement -= x_movement
    
y_movement = Vector2(0, input_movement.y)
if collision(player, element, y_movement):
    player_movement -= y_movement

if collision(player, element,player.momentum):
    player.momentum = Vector2(0,0)

if player_movement == player.momentum:
    break
'''