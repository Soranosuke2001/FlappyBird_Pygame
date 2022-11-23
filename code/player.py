import pygame
from gamesettings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, scaling):
        super().__init__(groups)

        # importing image of kirby
        kirby_Img = pygame.image.load('../images/player/kirby.png').convert_alpha()
        kirby_Img_Scaled = pygame.transform.scale(kirby_Img, pygame.math.Vector2(kirby_Img.get_size()) * scaling)
        self.image = kirby_Img_Scaled
        self.rect = self.image.get_rect(midleft = (window_Width / 20, window_Height / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, delta_Time):
        pass