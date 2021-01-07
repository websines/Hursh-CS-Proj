# imports
import sys
import pygame
from pygame.locals import (
        K_ESCAPE,KEYUP,KEYDOWN)
# my modules
import sprites 
from settings import Settings

pygame.init()
 
fpsClock = pygame.time.Clock()
settings = Settings() 
screen = pygame.display.set_mode((settings.width, settings.height))

playerGroup = pygame.sprite.Group()

yellowPlayer = sprites.Angel('yellow',[110,210])
#greenPlayer = sprites.Player('green',[110,210])
playerGroup.add(yellowPlayer)#,greenPlayer)
print(playerGroup.sprites())
screen_rect = screen.get_rect()
# Game loop.
run = True
print(screen_rect)
while run:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            for player in playerGroup.sprites():
                player.start_move(event)
            if event.key == K_ESCAPE:
                run = False
        if event.type == KEYUP:
            for player in playerGroup.sprites():
                player.stop_move(event)
            

    screen.fill((100, 100, 100))
    playerGroup.update()
    playerGroup.draw(screen)

    pygame.display.flip()
    fpsClock.tick(settings.fps)

pygame.quit()
print('game ended')
