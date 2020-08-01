from src.game_objects.resources import GameObject
from src.functions.sprite_sheet import spritesheet
from src.helpers.hashmap import HashTable
import pygame
from pygame import Vector2


class ChunkManager(HashTable):
    def __init__(self, graphic, sprite_object, filename, render_dist=1):
        super().__init__(filename)
        self.center_chunk = Vector2()
        self.render_dist = render_dist
        self.graphic = graphic
        self.sprite_object = sprite_object
        self.ss = spritesheet(graphic['file'])
        self.loaded_chunks = {}
        self.tiles = {}
    
    def set_center_chunk(self, global_center_pos):
        center_chunk = self.subchunk_point(global_center_pos)
        if self.center_chunk != center_chunk:
            self.center_chunk = center_chunk
            return True
        return False

    def update_tiles(self):
        loaded_chunks = []            
        min_render = self.center_chunk - Vector2(self.render_dist,self.render_dist)
        if self.render_dist > 1:        
            max_render = self.center_chunk + Vector2(self.render_dist,self.render_dist)
        else:
            max_render = Vector2(self.center_chunk) + Vector2(1)
        
        # TODO: x and y > 512 or <0  break the game
        for x in range(int(min_render.x), int(max_render.x)):
            for y in range(int(min_render.y), int(max_render.y)):
                local_chunk = self.chunks[x][y]  # Load Chunk hash  
                loaded_chunks.append(local_chunk)
        return loaded_chunks

    def update(self, chunks,  position):
        tiles = {}
        for chunk_id in chunks:
            if chunk_id in self.elements:
                for hash_id, element in self.elements[chunk_id].items():                 
                    if hash_id not in self.tiles:           
                        image_location = self.graphic['elements'][element['type']]['position']
                        image_rect = pygame.Rect(Vector2(image_location) * 32, [32,32])
                        tile_graphic = self.ss.image_at(image_rect, -1)

                        global_pos = Vector2(element['position'])
                        local_pos = position(global_pos)
                        tiles[hash_id] = self.sprite_object(local_pos, global_pos, tile_graphic)
                    else:
                        element = self.tiles[hash_id]
                        local_pos = position(element.global_pos)
                        element.position = local_pos
                        tiles[hash_id] = element
        self.tiles = tiles
        return tiles.values()