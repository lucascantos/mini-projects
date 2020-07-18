
from random import random, seed
from configs.game_state import SCREEN_DIM, screen_center
from helpers import round_vector
from map_generator import generate_fractal_noise_2d


import pygame
from pygame import Vector3, Vector2

pygame.init()
pygame.font.init()


screen = pygame.display.set_mode(round_vector(SCREEN_DIM))
pygame.display.set_caption("Perlin")
clock = pygame.time.Clock()
run =True

# perlin =  generate_perlin_noise_2d([size,size], [res,res],10)
perlin = generate_fractal_noise_2d([size,size], [res,res], octave, p)
perlin = normalized(perlin)



max_zoom = 20
zoom = 2
offset = Vector2()
target = SCREEN_DIM/4

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            pass
        if event.type == pygame.KEYUP:
            pass
    

    off_move = 1
    offset = Vector2()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        offset += Vector2(1,0) * off_move
    if keys[pygame.K_d]:
        offset += Vector2(-1,0) * off_move
    if keys[pygame.K_w]:
        offset += Vector2(0,1) * off_move
    if keys[pygame.K_s]:
        offset += Vector2(0,-1) * off_move
    
    if keys[pygame.K_r]:
        zoom = 2
        offset = Vector2()
        target = SCREEN_DIM/4
    target -= offset

    if keys[pygame.K_q]:
        if zoom > 2:
            zoom -= 1
    if keys[pygame.K_e]:
        if zoom < max_zoom:
            zoom += 1
    
    screen.fill((180,180,160))

    for x in range(size):
        for y in range(size):   
            # position = (Vector2(x,y) + offset)*zoom 

            position = screen_center + zoom*(Vector2(x,y) - target) 
            if position.x < -zoom or position.x > SCREEN_DIM.x:
                continue
            elif position.y < -zoom or position.y > SCREEN_DIM.y:
                continue
            

            if Vector2(x,y) == target:
                color = Vector3(255,0,0)
            else:
                wave = sinoid(x,size/2) *sinoid(y,size/2)
                value = perlin[x][y] * wave if wave <=1 else perlin[x][y]
                for h, c in height_color_map.items():
                    if value <= h:
                        hue = c
                        break

                seed(y*x)
                if value <= 0.3:
                    pass
                elif 0.35 <= value <= 0.4:
                    if random() < 0.2 - (value):
                        hue = tree
                    elif random() < 0.01:
                        hue = rock
                elif value <= 0.7:
                    if random() < 0.45 - (value/1.2):
                        hue = tree
                    elif random() < 0.001:
                        hue = rock
                elif value <= 0.9:
                    if random() < (value - 0.9) * -0.1/0.2:
                        hue = tree

                    elif random() < 0.01:
                        hue = rock
                        
                # if  0.9 >= value >= 0.3:
                #     value = (1-value) + 0.4

                color = hue

            screen.set_at(round_vector(position), color)
            sq = pygame.Rect(position, Vector2(max_zoom))
            pygame.draw.rect(screen, color, sq)

    pygame.display.update()
    clock.tick(60)