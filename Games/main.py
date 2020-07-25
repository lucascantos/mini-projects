def main():
    from src.functions.simple_screen import InteractiveScreen, Rectangle

    from src.configs.perlin_map import size, res, octave, p
    from src.configs.color_map import height
    from src.functions.map_generator import PerlinNoise

    from src.game_objects.resources import Character
    from src.configs.animations import martha_a

    from pygame import Vector2, Vector3
    import pygame

    octave = 3
    max_res = 9
    size = 128
    s = 4
    
    perlin = PerlinNoise(size, max_res, seed=10)
    new_screen = InteractiveScreen()
    perlin.offset = Vector2(-4,-3.5)
    
    martha = Character(Vector2(), martha_a)
    while new_screen.toggle_run:
        from pygame import Vector2
        import pygame

        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.toggle_run = False

        keys = pygame.key.get_pressed()
        zoom_level = 0
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
                d = {
                    -1: 3,
                    0: 1,
                    1: 0,
                    2: 2,
                    -2: 2,
                }
                martha.look_dir = d[round(offset.as_polar()[1]/90)]

        if keys[pygame.K_SPACE]:
            martha.state = 'attack'

            
        # Update
        if zoom_level != 0 :
            perlin.value += zoom_level
            if max_res-1 >= perlin.value >= octave:
                print(max_res-1, perlin.value, octave)
                perlin.set_zoom()
            else:
                perlin.value -= zoom_level

        if offset != Vector2():
            perlin.offset += offset/2
        pln = perlin.normalized(perlin.fractal(octave)) * perlin.sigmoid(threshold=16, smooth=.4)

        
        # Render 
        # new_screen.all_sprites = [martha]

        elements = []
        for x in range(0,size):
            for y in range(0,size):
                color = pln[x][y] * Vector3(255,255,255)
                for h, color in height.items():
                    if pln[x][y]<=h:
                        break
                elements.append(Rectangle(Vector2(x,y)*s, Vector2(1,1)*s, color * pln[x][y]))
        # print(perlin.offset, perlin.value)
        for i in elements:
            pygame.draw.rect(new_screen.screen, i.color, i.shape)
        # allsprites.draw(new_screen)
        new_screen.run()

if __name__ == "__main__":
    main()