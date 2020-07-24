def main():
    from src.configs.perlin_map import size, res, octave, p
    from src.functions.simple_screen import InteractiveScreen, Rectangle
    from src.configs.color_map import height
    from src.functions.map_generator import PerlinNoise
    from src.game_objects import resources
    from src.configs import animations

    from pygame import Vector2, Vector3
    import pygame

    octave = 3
    max_res = 9
    size = 128
    s = 4
    
    perlin = PerlinNoise(size, max_res, seed=10)
    new_screen = InteractiveScreen()
    perlin.offset = Vector2(-4,-3.5)
    
    martha = resources.Character(Vector2(), animations.martha)
    print(martha.animations)
    sprite_direction = 0
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
        
        offset = Vector2()
        martha.state = 'idle'
        if keys[pygame.K_w]:
            offset.y -= 1
            martha.state = 'walk'
        if keys[pygame.K_s]:
            offset.y += 1
            martha.state = 'walk'
        if keys[pygame.K_a]:
            offset.x -= 1
            martha.state = 'walk'
        if keys[pygame.K_d]:
            offset.x += 1
            martha.state = 'walk'
        if offset != Vector2():
            d = {
                -1: 3,
                0: 1,
                1: 0,
                2: 2,
                -2: 2,
            }
            sprite_direction = d[round(offset.as_polar()[1]/90)]

        if keys[pygame.K_SPACE]:
            martha.state = 'attack'
        # Update
        # if zoom_level != 0 :
        #     perlin.value += zoom_level
        #     if max_res-1 >= perlin.value >= octave:
        #         print(max_res-1, perlin.value, octave)
        #         perlin.set_zoom()
        #     else:
        #         perlin.value -= zoom_level

        # if offset != Vector2():
        #     perlin.offset += offset/2
        # pln = perlin.normalized(perlin.fractal(octave))


        martha.image_index += 1
        
        # Render 
        if len(martha.animations[martha.state][sprite_direction]) <= martha.image_index:
            martha.image_index = 0
        martha.image = martha.animations[martha.state][sprite_direction][martha.image_index]
        martha.rect = martha.image.get_rect()
        elements = [martha]
        # for x in range(0,size):
        #     for y in range(0,size):
        #         color = pln[x][y] * Vector3(255,255,255)
        #         for h, color in height.items():
        #             if pln[x][y]<=h:
        #                 break
        #         elements.append(Rectangle(Vector2(x,y)*s, Vector2(1,1)*s, color))
        # print(perlin.offset, perlin.value)

        # allsprites.draw(new_screen)
        new_screen.render(elements)
        new_screen.run()

if __name__ == "__main__":
    main()