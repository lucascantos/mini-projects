from src.game_objects.resources import GameObject
from src.functions.sprite_sheet import spritesheet
from src.helpers.hashmap import HashTable
import pygame
from pygame import Vector2


class ChunkManager(HashTable):
    def __init__(self, graphic, filename, render_dist=1):
        super().__init__(filename)
        self.center_chunk = Vector2()
        self.render_dist = render_dist
        self.graphic = graphic
        self.ss = spritesheet(graphic['file'])
        self.loaded_chunks = {}
        self.tiles = []
    
    def set_center_chunk(self, global_center_pos):
        center_chunk = self.subchunk_point(global_center_pos)
        if self.center_chunk != center_chunk:
            self.center_chunk = center_chunk
            return True
        return False

    def update_tiles(self):
        loaded_chunks = {}
            
        min_render = self.center_chunk - Vector2(self.render_dist,self.render_dist)
        if self.render_dist > 1:        
            max_render = self.center_chunk + Vector2(self.render_dist,self.render_dist)
        else:
            max_render = Vector2(self.center_chunk) + Vector2(1)
        
        # TODO: x and y > 512 or <0  break the game
        for x in range(int(min_render.x), int(max_render.x)):
            for y in range(int(min_render.y), int(max_render.y)):
                local_chunk = self.chunks[x][y]  # Load Chunk hash  
                if local_chunk in self.loaded_chunks.keys():
                    loaded_chunks[local_chunk] = self.loaded_chunks[local_chunk]
                else:
                    if local_chunk in self.elements:  # Check if chunk hash is mapped
                        loaded_chunks[local_chunk] = self.elements[local_chunk]
        self.loaded_chunks = loaded_chunks
        
    def update(self, func, *args, **kwargs,):
        tiles = {}
        for chunk in self.loaded_chunks.values():
            for hash_id, element in chunk.items():
                if hash_id not in self.tiles:
                    update = False
                else:
                    update = True
                    element = self.tiles[hash_id]

                tiles[hash_id] = func(*args+(element, update), **kwargs)
                tiles[hash_id].hash_id = hash_id
        self.tiles = tiles
        print(self.elements)
        return self.tiles.values()

    def make_graphics(self, center_local_pos, center_global_pos, element, update=False):  
        if update:    
            local_pos = center_local_pos - (center_global_pos - element.global_pos) * 32
            element.position = local_pos
            return element
        else:  
            image_location = self.graphic['elements'][element['type']]['position']
            image_rect = pygame.Rect(Vector2(image_location) * 32, [32,32])
            tile_graphic = self.ss.image_at(image_rect, -1)

            global_pos = Vector2(element['position'])
            local_pos = center_local_pos - (center_global_pos - global_pos) * 32
            return GraphicTile(local_pos, global_pos, tile_graphic)


    def make_collision(self, element, center_local_pos, center_global_pos,update=False, **kwargs):  
        if update:    
            local_pos = center_local_pos - (center_global_pos - element.global_pos) * 32
            element.position = local_pos
            return element
        else:  
            global_pos = Vector2(element['position'])
            local_pos = center_local_pos - (center_global_pos - global_pos) * 32
            return CollisionShape(local_pos, global_pos, **kwargs)

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

class GraphicTile(SpriteTile):
    def __init__(self, local_pos, global_pos, graphic):
        super().__init__(local_pos, global_pos)
        self.image = graphic

class CollisionShape(SpriteTile):
    def __init__(self, local_pos, global_pos, radius=None):
        super().__init__(local_pos, global_pos)
        if radius is not None:
            self.radius = radius    

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

