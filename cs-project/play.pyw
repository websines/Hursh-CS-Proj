#imports game modules
from multiplayerGame.network import Network
import sys
import pygame
import pickle
import numpy
import random
from pygame.locals import *
# import my modules
import sprites
import level
from settings import *
import mapLoader
import mapEditor
import FontRenderer
from network import Network
#from gameMenu import Menu

# order for the players will always remain
# A1, G1, A2, G2, A3, G3 ...
class MenuBlocks(pygame.sprite.Sprite):
    def __init__(self,img,pos,val):
        super().__init__()
        self.image = pygame.image.load(r'./OtherData/' + img).convert()
        self.image.set_colorkey("#000000")
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.value = val

class Game:
    def __init__(self):
        #---------------- PYGAME STUFF ------------------#
        self.settings = Settings()
        self.displaySize = self.settings.getDisplaySize()
        #self.screen = pygame.Surface((self.settings.width,self.settings.height))
        self.screen = pygame.display.set_mode((self.settings.width,self.settings.height),FULLSCREEN)
        self.fpsClock = pygame.time.Clock()
        self.homeScreen()
    
    def newGame(self, peers):
        #---------------- SPRITE STUFF ------------------#
        self.playerGroup = pygame.sprite.Group()
        self.addAllPlayers()
        self.peers = peers
        self.net = Network()
        #---------------- MAP INIT STUFF ----------------#
        level = 1 #self.startScreen()
        self.map = mapLoader.Map(level)
        self.bg = pygame.image.load(r'./WorldData/Level '+str(level)+r'/bg.png')
        #---------------- GAME RUNTIME STUFF ------------#
        self.running = True
        self.cam = pygame.math.Vector2(1.0,0.0)
        self.focus = [(self.settings.width + self.player.rect.width) // 2,(self.settings.height + self.player.rect.height) // 2]
        self.mainloop()

    def addAllPlayers(self):
        c = 0
        for location in [(50,50),(100,100),(150,150)][:self.peers]:
            a = sprites.Angel(c,location)
            c += 1
            if self.net.id == c:
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

    def update(self):
        #---------------- player updates ------------#
        self.move(self.map.group)
        self.cam[0] += (self.player.rect.x - self.cam[0] - self.focus[0])/20
        self.cam[1] += (self.player.rect.y - self.cam[1] - self.focus[1])/20
        self.cam[0] = int(self.cam[0])
        self.cam[1] = int(self.cam[1])
        self.map.group.update()
        self.player.update()
        self.update_pos()
        #---------------- MAP UPDATES ---------------#
        if self.player.rect.y >= self.settings.height * 2:
            self.player.rect.topleft = random.choice([(0,0),(1000,0),(1700,0)])
            self.player.physics.vel = pygame.math.Vector2(0.0,0.0)

    def update_pos(self):
        self.players_pos = pickle.loads(self.net.send(pickle.dumps([self.net.id,(self.player.rect.x,self.player.rect.y)])))
        for player,pos in zip(self.playerGroup,self.players_pos):
            player.rect.x,player.rect.y = pos

    def blitAndFlip(self):
        self.display.fill("#101010")
        self.display.blit(pygame.transform.scale(self.screen,self.displaySize),(0,0))
        pygame.display.flip()

    def drawPlayers(self):
        for player in self.playerGroup.sprites():
            self.screen.blit(player.image,(player.rect.x - self.cam[0],player.rect.y - self.cam[1]))

    def draw(self):
        # fill with black
        self.screen.blit(self.bg,(0,0))
        # draw environment
        self.map.draw(self.screen, self.cam)
        # draw players
        self.drawPlayers()
        #self.screen.blit(self.player.image,self.player.rect)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            if event.type == KEYDOWN:
                    self.player.start_move(event)
                    if event.key == K_ESCAPE:
                        self.homeScreen()
                        self.running = False
                    if event.key == K_DOWN: self.player.dash()
                    if event.key == K_SPACE or event.key == K_UP or event.key == K_w: self.player.jumping = True
            if event.type == KEYUP:
                    self.player.stop_move(event)
                    if event.key == K_SPACE or event.key == K_UP or event.key == K_w:
                        self.player.jumping = False
                    if event.key == K_RETURN: return K_RETURN

    def collisionDetect(self,entity,group):
        for entity2 in group.sprites():
            if entity2.value:
                if entity.rect.colliderect(entity2.rect):
                    return entity2

    # group is that of platforms with which the player interacts
    def move(self,group):
        self.player.colliding = {'top':False,'bottom':False,'left':False,'right':False}
        self.player.move_x()
        s = self.collisionDetect(self.player,group)
        if s:
            if self.player.physics.vel.x > 0:
                self.player.colliding['right'] = True
                self.player.rect.right = s.rect.left
            elif self.player.physics.vel.x < 0:
                self.player.colliding['left'] = True
                self.player.rect.left = s.rect.right
        self.player.move_y()
        s = self.collisionDetect(self.player,group)
        if s:
            if self.player.physics.vel.y > 0:
                self.player.colliding['bottom'] = True
                self.player.rect.bottom = s.rect.top
            elif self.player.physics.vel.y < 0:
                self.player.colliding['top'] = True
                self.player.rect.top = s.rect.bottom
        return s

    def editor(self):
        editor = mapEditor.MapEditor()
        pass

    def homeScreen(self):
        self.home = True
        self.bg = pygame.image.load('./OtherData/home.png')
        selected = 9
        self.homeGroup = pygame.sprite.Group()
        self.player = sprites.Angel([633,100],'#ec565c')
        for i in [('options.png',(55,533),1),('play.png',(480,513),2),('exit.png',(889,533),3),('T.png',(632,154),9)]:
            self.homeGroup.add(MenuBlocks(i[0],i[1],i[2]))
        t = 1
        def changeSelected(x,selected):
            for homeButton in self.homeGroup:
                if homeButton is x:
                    selected = homeButton.value
                if selected == homeButton.value:
                    homeButton.image.set_alpha(255)
                else:
                    homeButton.image.set_alpha(180)
            return selected

        while self.home:
            self.screen.blit(self.bg,(0,0))
            pressed = self.handleEvents()
            s =self.move(self.homeGroup)
            selected = changeSelected(s, selected)
            K = pygame.key.get_pressed()
            if pressed == K_RETURN:
                    if selected == 1: self.editor()
                    if selected == 2: self.newGame()
                    if selected == 3:
                        self.home = False
                        self.screen.fill("#000000")

            self.player.update()
            self.screen.blit(self.player.image,self.player.rect.topleft)
            self.homeGroup.draw(self.screen)
            pygame.display.update()
            self.fpsClock.tick(self.settings.fps)
        self.player.kill()

    def startScreen(self):
        ques = FontRenderer.CenteredText('MAP TO PLAY?',(500,300),textSize = 30)
        warningNum = FontRenderer.CenteredText('*Level should be numeric',(600,500))
        IN = FontRenderer.Button('   ',(900,300))
        level = ''
        while True:
            print('start')
            self.screen.fill("#101010")
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        level = level[:-1]
                    else:
                        level += event.unicode
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        self.fadeIn()
                        pygame.quit()
                        sys.exit()
                    if event.key == K_RETURN:
                        val = int(level)
                        if val in [1,2,3]:
                            self.fadeIn()
                            return val
                        else:
                            self.fadeIn()
                            self.sorry('Sorry, that level is not Available.')

            IN.renderFonts(level)
            IN.draw(self.screen)
            ques.draw(self.screen)
            if not level.isnumeric():
                warningNum.draw(self.screen)

    def sorry(self,text):
        messege = FontRenderer.CenteredText(text,(500,300))
        running = True
        while running:
            self.screen.fill('#101010')
            messege.draw(self.screen)
            for event in pygame.event.get():
                if event.type == KEYUP:
                    if event.key == K_RETURN or event.key == K_ESCAPE:
                        self.fadeIn()
                        return

    def fadeIn(self):
        fadePad = pygame.Surface((self.settings.width,self.settings.height))
        fadePad.fill("#101010")
        alpha = 40
        while True:
            alpha += 11
            if alpha > 255:
                break
            fadePad.set_alpha(alpha)
            self.screen.blit(fadePad,(0,0))
            pygame.display.flip()
            pygame.time.delay(2)
        self.screen.fill("#101010")
        pygame.time.delay(50)

if __name__ == "__main__":
    game = Game()
    pygame.quit()
