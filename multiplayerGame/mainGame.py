#imports game modules
import sys
import pygame
import pickle
from pygame.locals import (
        K_ESCAPE,KEYUP,KEYDOWN,K_k)
# import my modules
import sprites
import Platforms
from settings import *
from network import Network
#from gameMenu import Menu

# order for the players will always remain
# A1, G1, A2, G2, A3, G3 ...
class Game:
    def __init__(self):
        self.net = Network()
        self.settings = Settings()
        self.fpsClock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.settings.width,self.settings.height))
        self.running = True
        # only useful for drawing Group
        self.playerGroup = pygame.sprite.Group()
        self.addAllPlayers()
        self.platforms = pygame.sprite.Group()
        self.addPlatforms()
        self.mainloop()
        #self.menu = Menu()

    def addAllPlayers(self):
        for i in range(self.settings.num_of_players):
            a = sprites.Angel(i,[120,203])
            self.playerGroup.add(a)
            if self.net.id == i:
                self.player = a

    def mainloop(self):
        while self.running:
            # handle, update and draw
            self.handleEvents()
            self.update()
            self.draw()
            # flip and tick
            pygame.display.update()
            self.fpsClock.tick(self.settings.fps)

    def move(self):
        self.player.colliding = {'top':False,'bottom':False,'left':False,'right':False}
        self.player.move_x()
        s = pygame.sprite.spritecollideany(self.player,self.platforms)
        if s:
            if self.player.physics.vel.x > 0:
                self.player.colliding['right'] = True
                self.player.rect.right = s.rect.left
            elif self.player.physics.vel.x < 0:
                self.player.colliding['left'] = True
                self.player.rect.left = s.rect.right
        self.player.move_y()
        s = pygame.sprite.spritecollideany(self.player,self.platforms)
        if s:
            if self.player.physics.vel.y > 0:
                self.player.colliding['bottom'] = True
                self.player.rect.bottom = s.rect.top 
            elif self.player.physics.vel.y < 0:
                self.player.colliding['top'] = True
                self.player.rect.top = s.rect.bottom

    def update_pos(self):
        self.players_pos = pickle.loads(self.net.send(pickle.dumps([self.net.id,(self.player.rect.x,self.player.rect.y)])))
        for player,pos in zip(self.playerGroup,self.players_pos):
            player.rect.x,player.rect.y = pos


    def update(self):
        # playerSprites_update
        self.move()
        # environment_update
        self.platforms.update()

        self.player.update()
        self.update_pos()

            

    def draw(self):
        # fill with black
        self.screen.fill((0,0,0))
        # draw environment
        self.platforms.draw(self.screen)
        # draw players
        self.update_pos()
        self.playerGroup.draw(self.screen)
        #self.screen.blit(self.player.image,self.player.rect)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                    self.player.start_move(event)
                    if event.key == K_ESCAPE:
                        self.running = False
                    if event.key == K_k:
                        self.player.jumping = True
            if event.type == KEYUP:
                    self.player.stop_move(event)
                    if event.key == K_k:
                        self.player.jumping = False

            #mousemotion events (for guardians)
            #mousebutton events (for guardians)


    def addPlatforms(self):
        self.platforms.add(Platforms.Platform(400,400))
        self.platforms.add(Platforms.Platform(0,self.settings.height-10,self.settings.width))
        self.platforms.add(Platforms.Platform(0,0,self.settings.width))
        self.platforms.add(Platforms.Platform(0,0,20,self.settings.height))
        self.platforms.add(Platforms.Platform(self.settings.width-20,0,20,self.settings.height))

    def homeMenu(self):
        #
        pass

    def start(self):
        # set running is true
        # running
        pass

if __name__ == "__main__":
    game = Game()
    pygame.quit()
