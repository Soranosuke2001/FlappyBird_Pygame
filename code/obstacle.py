import pygame
from random import choice, randint
from gamesettings import *

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups, scaling, position):
        super().__init__(groups)
        self.sprite_Type = 'pipe'

        pipe_Img = pygame.image.load('../images/background/game/pipe.png').convert_alpha()
        self.image = pygame.transform.scale(pipe_Img, pygame.math.Vector2(pipe_Img.get_size()) * scaling)
        self.rect = self.image.get_rect()

        pipe_Offset = randint(200, 400)
        pipe_Start = window_Width + (window_Width / 20)
        center_Y = window_Height / 2

        if position == 'up':
            self.rect.midtop = [pipe_Start, center_Y + pipe_Offset]
        if position == 'down':
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.midbottom = [pipe_Start, center_Y - pipe_Offset]

    def update(self, delta_Time):
        self.rect.x -= 300 * delta_Time
        if self.rect.right <= -100:
            self.kill()



