def main():
    '''
    TODO: 
    Update Animation with FPS
    Add Interactions
    Add Items DB
    Add AI
    Add Dynamic Camera

    DOING:
    Update Hashtable (split chunks and elements)
    
    Add Collision

    DONE:
    fix border and fps drop
    fix alpha sprites
    '''
    from src.functions.simple_screen import InteractiveScreen, Rectangle
    from src.configs.color_map import height

    from src.game_objects.resources import Character, Placehodler
    from src.game_objects.terrain import ChunkManager
    from src.configs.animations import characters, tileset
    from src.helpers.hashmap import HashTable

    from pygame import Vector2, Vector3
    import pygame

    
    new_screen = InteractiveScreen()  
    martha = Character(Vector2(new_screen.center), Vector2(253, 538), characters['martha'])
    render_dist = 5 # In Chunks
    
    # TODO: about camera and stuff
    bg_map = ChunkManager(tileset, 'terrain', render_dist)
    resources = ChunkManager(tileset, 'resources', render_dist)

    collision_objects = ChunkManager(tileset, 'resources', 1)

    while new_screen.toggle_run:
        from pygame import Vector2
        import pygame

        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.toggle_run = False

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
                martha.move(5*offset/new_screen.clock.get_fps())
            if keys[pygame.K_SPACE]:
                martha.state = 'attack'
                martha.image_index = 0
        
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

        if bg_map.set_center_chunk(martha.global_pos): 
            resources.set_center_chunk(martha.global_pos)
            print('Update')
            bg_map.update_tiles()
            resources.update_tiles()        

        j = list(bg_map.update(bg_map.make_graphics, martha.position, martha.global_pos))
        k = list(resources.update(resources.make_graphics, martha.position, martha.global_pos))

        deleted = pygame.sprite.spritecollide(martha, pygame.sprite.RenderPlain(k), True)

        for d in deleted:
            print(d)
            resources.remove_element(d.hash_id)

        zindex = lambda x: x.position[1]
        k += [martha]
        k.sort(key=zindex)
        new_screen.all_sprites = j + k
        new_screen.run()
if __name__ == "__main__":
    main()