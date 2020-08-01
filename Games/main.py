def main():
    '''
    TODO: 
    Update Animation with FPS
    Update Collisions to x/y
    update movement speed
    
    Add Interactions
    Add Items DB
    Add AI
    Add Dynamic Camera

    DOING:

    DONE:
    Update Hashtable (split chunks and elements)    
    Add Collision
    fix border and fps drop
    fix alpha sprites
    '''
    from src.functions.simple_screen import InteractiveScreen, Rectangle
    from src.configs.color_map import height

    from src.game_objects.resources import Character, Placehodler, TerrainTile, ResourcesTile, CircleCollision
    from src.game_objects.terrain import ChunkManager
    from src.configs.animations import characters, tileset
    from src.helpers.hashmap import HashTable

    from pygame import Vector2, Vector3
    import pygame

    
    new_screen = InteractiveScreen()  
    render_dist = 3 # In Chunks

    martha = Character(Vector2(new_screen.center), Vector2(253, 538), characters['martha'])
    relative_position = lambda x: martha.position - (martha.global_pos - x) * 32
    
    # TODO: about camera and stuff
    bg_map = ChunkManager(tileset, TerrainTile, 'terrain', render_dist)
    resources = ChunkManager(tileset, ResourcesTile, 'resources', render_dist)
    avg = 0


    def circle_collider(sprite):
        """Check if the hitboxes of the two sprites collide."""
        return CircleCollision(sprite.position, sprite.radius)
    
    def walk_collision(sprite, other):
        return pygame.sprite.collide_circle(circle_collider(sprite), circle_collider(other))

    while new_screen.toggle_run:
        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                new_screen.toggle_run = False

        keys = pygame.key.get_pressed()
        # zoom_level = 0
        if keys[pygame.K_q]:
            zoom_level = -1
        if keys[pygame.K_e]:
            zoom_level = 1
        
        if martha.state == 'idle' or martha.state == 'walk':
            offset = Vector2()
            new_state = 'idle'
            if keys[pygame.K_w]:
                offset.y -= 1
                new_state = 'walk'
            if keys[pygame.K_s]:
                offset.y += 1
                new_state = 'walk'
            if keys[pygame.K_a]:
                offset.x -= 1
                new_state = 'walk'
            if keys[pygame.K_d]:
                offset.x += 1
                new_state = 'walk'

            martha.state = new_state
            if offset != Vector2():
                polar_2_index = {
                    -1: 3,
                    0: 1,
                    1: 0,
                    2: 2,
                    -2: 2,
                }
                martha.look_dir = polar_2_index[round(offset.as_polar()[1]/90)]
                fps = new_screen.clock.get_fps() if new_screen.clock.get_fps() > 0 else 1
                rel_offset = 5 * offset/fps
                martha.move(rel_offset)
            if keys[pygame.K_SPACE]:
                martha.state = 'attack'
                martha.image_index = 0
        
        relative_position = lambda x: martha.position - (martha.global_pos - x) * 32
        # Update 
        '''
        group moving objects (players, creatures, emtities, etc)
        group collision objects (terrain, characters, entities, objects, etc)
        around every MO, load 1 chunk worth of CO
        check for collisions on all MO

        Maybe add subgroups o updated objects
        '''
        # if collision_objects.set_center_chunk(martha.global_pos):
        #     collision_objects.update_tiles()   
        # col_list = list(collision_objects.update(collision_objects.make_collision, martha.position, martha.global_pos))
        
        #TODO Check if camera changed chunk, no bg_map
        if bg_map.set_center_chunk(martha.global_pos): 
            print('Update')
            loaded_chunks = bg_map.update_tiles() 
            resources.set_center_chunk(martha.global_pos)

        
        from time import time
        start = time()
        j = list(bg_map.update(loaded_chunks, relative_position))
        k = list(resources.update(loaded_chunks, relative_position))

        end = round((time() - start)*1000,2)
        avg = (avg + end) / 2
        # print(avg) if avg > 7 else None

        deleted = pygame.sprite.spritecollide(martha, pygame.sprite.RenderPlain(k), True, walk_collision)
        if len(deleted) > 0:
            martha.move(-rel_offset)
            print(deleted)

        zindex = lambda x: x.position[1]

        k += [martha]
        k.sort(key=zindex)
        new_screen.all_sprites = j + k
        new_screen.run()

if __name__ == "__main__":
    main()