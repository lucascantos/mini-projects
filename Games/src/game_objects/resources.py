import pygame
from pygame import Vector2

from src.functions.sprite_sheet import spritesheet
# from game_objects.character import Head
class GameObject(pygame.sprite.Sprite):
    def __init__(self, size, position):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(Vector2(), size) # Square to be draw uppon
        self.rect.center = position # Adjust local position to be center
        self.collision_box = None # List of masks to be applied

    @property
    def position(self):
            return self.rect.center            
    @property
    def width(self):
        return self.canvas.get_width()
    @property
    def height(self):
        return self.canvas.get_height()
    

class Character(GameObject):
    def __init__(self, position, global_pos, graphics):
        super().__init__(Vector2(32,32),position) 

        self.animations = {} # Animations of object
        self.state = 'idle'
        self.image_index = 0 # Current frame index
        self.image = None # Current frame to show

        self.global_pos = global_pos
        top_center = Vector2(self.rect.center)
        top_center.y /= 2
        top_center -= top_center / 2

        bot_center = Vector2(self.rect.center)
        bot_center.y *= 1.5
        bot_center -= bot_center / 2

        self.collision_box = [
            pygame.Rect(top_center,  Vector2(self.rect.size) / 2 ),
            pygame.Rect(bot_center,  Vector2(self.rect.size) / 2 )
        ]
        self.animations = self.make_animations(graphics, 4)
        self.look_dir = 0

    def update(self):
        if len(self.animations[self.state][self.look_dir])-1 <= self.image_index:
            self.image_index = 0
        else:
            self.image_index += 1

        if self.state == 'idle' or self.state == 'walk':
            self.image = self.animations[self.state][self.look_dir][self.image_index]
        else:
            self.image = self.animations[self.state][self.look_dir][self.image_index]
            if len(self.animations[self.state][self.look_dir])-1 <= self.image_index:
                self.state = 'idle'
                
    def move(self, offset):
        # check if bottom collision is true
        self.global_pos += offset

    def make_animations(self, animation_info, directions):
        '''
        Create animation dictionary with all elements already in place and loaded
        '''
        animation_sheet = []
        if animation_info['type'] == 'sheet':
            x,y = animation_info['size']
            for row in range(directions):
                single_frame = pygame.Rect([0,y*row], [x,y])
                ss = spritesheet(animation_info['file'])
                animation_sheet.append(ss.load_strip(single_frame, 6, -1))

        elif animation_info['type'] == 'files':
            pass

        output = {}
        for name, value in animation_info['actions'].items():   
            all_dir = []          
            if value['duration'] is None:       
                all_dir = [ [animation_sheet[d][value['frame']]] for d in range(directions)]
            else:
                for d in range(directions):
                    single_dir = []
                    for frame, duration in zip(value['frame'], value['duration']):
                        single_dir += [animation_sheet[d][frame] for _ in range(duration)]
                    if value['rock']:
                        upper_bound = len(single_dir)-(1*value['duration'][-1])
                        lower_bound = value['duration'][0]
                        single_dir += [ single_dir[i] for i in range(upper_bound, lower_bound,-1)]
                    all_dir.append(single_dir)
            output[name] = all_dir
        return output

class Player(Character):
    def __init__(self):
        super().__init__()

class Placehodler(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('src/assets/placeholder.png')
        self.rect = pygame.Rect(Vector2(), [16,16])
        self.rect.center = position
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