import pygame
from gamesettings import *

class Background(pygame.sprite.Sprite):
    def __init__(self, groups, scaling):
        super().__init__(groups)

        # importing the background image and scaling it to fit the window size
        bkg_Img = pygame.image.load('../images/background/game/background.jpg').convert()

        width_Scaled = bkg_Img.get_width() * scaling
        height_Scaled = bkg_Img.get_height() * scaling

        bkg_Img_Scaled = pygame.transform.scale(bkg_Img, (width_Scaled, height_Scaled))
        self.image = pygame.Surface((width_Scaled * 2, height_Scaled))

        # displaying the background image on the window, and printing 2 to double the width
        self.image.blit(bkg_Img_Scaled, (0, 0))
        self.image.blit(bkg_Img_Scaled, (width_Scaled, 0))

        self.rect = self.image.get_rect(topleft = (0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, delta_Time):
        self.pos.x -= 300 * delta_Time

        if self.rect.centerx <= 0:
            self.pos.x = 0
        
        self.rect.x = round(self.pos.x)


