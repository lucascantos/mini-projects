import pygame
from pygame import Vector2

from src.functions.sprite_sheet import spritesheet
# from game_objects.character import Head


class SpriteTile(pygame.sprite.Sprite):
    def __init__(self, local_pos, global_pos, size = [32,32]):
        pygame.sprite.Sprite.__init__(self)
        self.global_pos = global_pos
        self.rect = pygame.Rect(local_pos, [32,32])
        self.position = local_pos
        
    def get_position(self):
        return self.rect.center
    def set_position(self, position):
        self.rect.center = position

    position = property(get_position, set_position)



class GameObject(pygame.sprite.Sprite):
    def __init__(self, size, position):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(Vector2(), size) # Square to be draw uppon
        self.rect.center = position # Adjust local position to be center
        self.collision_box = None # List of masks to be applied

        self.global_pos = Vector2()
        self.center_rel_pos = lambda x: self.position - (self.global_pos - x) * 32

    def get_position(self):
        return self.rect.center
    def set_position(self, position):
        self.rect.center = position
    position = property(get_position, set_position)

    @property
    def width(self):
        return self.canvas.get_width()
    @property
    def height(self):
        return self.canvas.get_height()
    

class Character(GameObject):
    def __init__(self, position, global_pos, graphics):
        super().__init__(Vector2(32,32),position) # Standard graphic size 32x32

        self.animations = {} # Animations of object
        self.state = 'idle'
        self.image_index = 0 # Current frame index
        self.image = None # Current frame to show

        self.global_pos = global_pos

        self.radius = int(32/4) # Radius of 1/4 the width

        self.speed = 0
        self.velocity = [0,0]
        collision_boxes = {
            'broadVision': {}, # diagonal square (diamond)
            'focusVision': {}, # narrow rectanle
            'periferalVision': {}, # wide oval
            'collision':{}, #base circle
            'interaction':{} # 2x size
        }
        
        self.animations = self.make_animations(graphics, 4) # 4 Directions of animation (W,N,E,S)
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
    
    def relative_position(self, position):
        return self.position - (self.global_pos - position) * 32

class TerrainTile(GameObject):
    def __init__(self, position, global_pos, graphic):
        super().__init__(Vector2(32,32), position)
        self.image = graphic
        self.global_pos = global_pos

class ResourcesTile(TerrainTile):
    def __init__(self, position, global_pos, graphic):
        super().__init__(position, global_pos, graphic)
        self.radius = int(32/4)

class CircleCollision(pygame.sprite.Sprite):
    def __init__(self,position, radius=None, size=[32,32]):
        self.rect = pygame.Rect([0,0], [16,16])
        self.rect.center = Vector2(position) + Vector2(0,int(size[1]/2))
        if radius is not None:
            self.radius = int(size[0]/4)



class Placehodler(pygame.sprite.Sprite):
    def __init__(self, position, global_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('src/assets/placeholder.png')
        self.rect = pygame.Rect(position, [16,16])
        self.rect.center = position
        self.global_pos = global_pos
    
    def get_position(self):
        return self.rect.center

    def set_position(self, position):
        self.rect.center = position
    position = property(get_position, set_position)
