# imports game modules
import sys
import pygame
from pygame.locals import (
        K_ESCAPE,KEYUP,KEYDOWN)
# import my modules
import sprites 
from settings import *
from gameMenu import Menu

class Game:
    def __init__(self):
        self.settings = Settings()
        self.fpsClock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((settings.width,settings.height))
        self.running = False
        #self.menu = Menu()

    def mainloop(self):
        while self.running:
            # handle, update and draw
            self.handleEvents()
            self.update()
            self.draw()
            # flip and tick
            pygame.display.flip()
            self.fpsClock.tick(settings.fps)

    def update(self):
        # playerSprites_update
        # environment_update
        #
        pass
    
    def draw(self):
        self.screen.fill((0,0,0)) #fill with black
        # draw environment
        # draw players
        pass

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                for player in playerGroup.sprites():
            #mousemotion events (for guardians)
            #mousebutton events (for guardians)
        pass

    def homeMenu(self):
        #
        pass

    def start(self):
        # set running is true
        # running


