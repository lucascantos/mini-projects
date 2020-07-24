def main():
    from configs.perlin_map import size, res, octave, p
    from simple_screen import InteractiveScreen, Rectangle
    from configs.color_map import height
    from map_generator import PerlinNoise
    from pygame import Vector2, Vector3
    import pygame

    octave = 3
    max_res = 9
    size = 128
    s = 4
    
    perlin = PerlinNoise(size, max_res, seed=10)
    new_screen = InteractiveScreen()

    perlin.offset = Vector2(-4,-3.5)
    while new_screen.toggle_run:

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
        if keys[pygame.K_w]:
            offset.y -= 1
        if keys[pygame.K_s]:
            offset.y += 1
        if keys[pygame.K_a]:
            offset.x -= 1
        if keys[pygame.K_d]:
            offset.x += 1

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
        pln = perlin.normalized(perlin.fractal(octave))

        # Render 
        elements = []
        for x in range(0,size):
            for y in range(0,size):
                color = pln[x][y] * Vector3(255,255,255)
                for h, color in height.items():
                    if pln[x][y]<=h:
                        break
                elements.append(Rectangle(Vector2(x,y)*s, Vector2(1,1)*s, color))
        print(perlin.offset, perlin.value)
        new_screen.render(elements)
        new_screen.run()

if __name__ == "__main__":
    main()