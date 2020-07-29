def main():
    from src.functions.simple_screen import InteractiveScreen, Rectangle
    from src.configs.color_map import height

    from src.game_objects.resources import Character, Placehodler
    from src.game_objects.terrain import TerrainTile, ResourceTile
    from src.configs.animations import characters, tileset
    from src.helpers.hashmap import HashTable

    from pygame import Vector2, Vector3
    import pygame

    
    new_screen = InteractiveScreen()  
    martha = Character(Vector2(new_screen.center), Vector2(251, 538), characters['martha'])

    
    # TODO: about camara and stuff
    my_map = TerrainTile(tileset)
    k=[]
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

        if my_map.set_center_chunk(martha.global_pos): 
            print('Update', len(k))
            my_map.update_tiles()
            
        k = []
        k += my_map.update(martha.position, martha.global_pos)
        zindex = lambda x: x.position[1]
        k += [martha]
        k.sort(key=zindex)
        new_screen.all_sprites = k
        new_screen.run()
if __name__ == "__main__":
    main()