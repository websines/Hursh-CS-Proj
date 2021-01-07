import sys
 
import pygame
from pygame.locals import *
import sprites 

pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

test_player = sprites.Player()

# Game loop.
e = 0
while True:
    if pygame.key.get_focused():
        print('you just want attention')
    try: 
        e = pygame.event.get()[-1]
        print(e.key)
        print(ord('a'))
        if e.type == KEYDOWN:
            if e.key == 27:
                print('escape pressed')
                pygame.quit()
                sys.exit()
    except:
        pass
    # Update.
    # Draw.
    screen.fill((100, 100, 100))
    pygame.display.flip()
    fpsClock.tick(fps)
