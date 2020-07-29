
        ## MAP TEST

    # from src.configs.perlin_map import size, res, octave, p
    # from src.functions.map_generator import PerlinNoise
    # perlin = PerlinNoise(size, max_res, seed=10)
    # perlin.offset = Vector2(-4,-3.5)
    # octave = 3
    # max_res = 9
    # size = 128
    # s = 4
        # if zoom_level != 0 :
        #     perlin.value += zoom_level
        #     if max_res-1 >= perlin.value >= octave:
        #         print(max_res-1, perlin.value, octave)
        #         perlin.set_zoom()
        #     else:
        #         perlin.value -= zoom_level

        # if offset != Vector2():
        #     perlin.offset += offset/2
        # print(perlin.offset)
        # pln = perlin.normalized(perlin.fractal(octave)) * perlin.sigmoid(threshold=16, smooth=.4)

        # elements = []
        # for x in range(0,size):
        #     for y in range(0,size):
        #         color = pln[x][y] * Vector3(255,255,255)
        #         for h, color in height.items():
        #             if pln[x][y]<=h:
        #                 break
        #         elements.append(Rectangle(Vector2(x,y)*s, Vector2(1,1)*s, color * pln[x][y]))
        # # print(perlin.offset, perlin.value)
        # for i in elements:
        #     pygame.draw.rect(new_screen.screen, i.color, i.shape)
        # allsprites.draw(new_screen)
        # new_screen.run()
