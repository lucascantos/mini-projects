from src.game_objects.resources import GameObject
from src.functions.sprite_sheet import spritesheet
from src.helpers.hashmap import HashTable
import pygame
from pygame import Vector2

class TerrainTile(HashTable):
    def __init__(self, graphic):
        super().__init__()
        self.center_chunk = Vector2()
        self.render_dist = 1
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
            max_render = Vector2(self.center_chunk)
        for x in range(int(min_render.x), int(max_render.x)+1):
            for y in range(int(min_render.y), int(max_render.y)+1):
                local_chunk = self.chunks[x][y]  # Load Chunk hash  
                if local_chunk in self.loaded_chunks.keys():
                    loaded_chunks[local_chunk] = self.loaded_chunks[local_chunk]
                else:
                    if local_chunk in self.elements:  # Check if chunk hash is mapped
                        loaded_chunks[local_chunk] = self.elements[local_chunk]
        self.loaded_chunks = loaded_chunks

    def update(self,center_local_pos, center_global_pos):

        tiles = {}
        for chunk in self.loaded_chunks.values():
            for hash_id, element in chunk.items():
                if hash_id not in self.tiles:
                    image_location = self.graphic['elements'][element['type']]['position']
                    image_rect = pygame.Rect(Vector2(image_location) * 32, [32,32])
                    tile_graphic = self.ss.image_at(image_rect)

                    global_pos = Vector2(element['position'])
                    local_pos = center_local_pos - (center_global_pos - global_pos) * 32
                    new_tile = ResourceTile(local_pos, global_pos, tile_graphic)
                    tiles[hash_id] = new_tile
                else:
                    element = self.tiles[hash_id]
                    local_pos = center_local_pos - (center_global_pos - element.global_pos) * 32
                    element.position = local_pos
                    tiles[hash_id] = element
        self.tiles = tiles
        return self.tiles.values()

class ResourceTile(pygame.sprite.Sprite):
    def __init__(self, local_pos, global_pos, graphic):
        pygame.sprite.Sprite.__init__(self)
        self.global_pos = global_pos
        self.image = graphic
        self.rect = pygame.Rect(local_pos, [32,32])
        self.position = local_pos

    def get_position(self):
        return self.rect.center
    def set_position(self, position):
        self.rect.center = position

    position = property(get_position, set_position)


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

