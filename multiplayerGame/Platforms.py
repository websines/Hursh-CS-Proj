import pygame
from HC_Verma import Physics
from settings import Settings
class Platform(pygame.sprite.Sprite):
    
    def __init__(self,pos_x,pos_y,width = 100,height=20):
        super().__init__()
        self.settings = Settings()
        self.image = pygame.Surface((width,height))
        self.image.fill('orange')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_x, pos_y
        self.physics = Physics(self.rect,1000)

    def update(self):
        #self.rect.x += 3
        if self.rect.left >= self.settings.width:
            self.rect.right = 0


