def main():
    from configs.perlin_map import size, res, octave, p
    from simple_screen import InteractiveScreen, Rectangle
    from configs.color_map import height
    from map_generator import PerlinNoise
    from pygame import Vector2, Vector3

    max_res = 8
    size = 128
    s = 4
    
    offset = max_res
    perlin = PerlinNoise([size,size], max_res, value=offset)
    pln = perlin.normalized(perlin.fractal(3))

    new_screen = InteractiveScreen()
    while new_screen.toggle_run:
        elements = []
        for x in range(0,size):
            for y in range(0,size):
                # color = pln[x][y] * Vector3(255,255,255)
                for h, color in height.items():
                    if pln[x][y]<=h:
                        break
                elements.append(Rectangle(Vector2(x,y)*s, Vector2(1,1)*s, color*pln[x][y]))
        new_screen.elements = elements
        output = new_screen.run()
        if output:
            offset += output
            # # Movement
            # perlin.offset = [offset, 0]

            # Zoom
            perlin.value = offset
            perlin.set_zoom()
            print(perlin.zoom)

            perlin.set_noise()
            pln = perlin.normalized(perlin.fractal(3))
        
if __name__ == "__main__":
    main()