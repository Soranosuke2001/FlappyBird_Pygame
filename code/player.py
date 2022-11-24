import pygame
from gamesettings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, scaling):
        super().__init__(groups)
        self.sprite_Type = 'player'

        # importing image of kirby
        kirby_Img = pygame.image.load('../images/player/kirby.png').convert_alpha()
        kirby_Img_Scaled = pygame.transform.scale(kirby_Img, pygame.math.Vector2(kirby_Img.get_size()) * scaling)
        self.image = kirby_Img_Scaled
        self.rect = self.image.get_rect(midleft = (window_Width / 20, window_Height / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # setting the player movements
        self.gravity = 600
        self.direction = 0

        # setting the mask for the player
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen_Size):
        screen_Size.blit(self.image, self.rect)

    def player_gravity(self, delta_Time):
        self.direction += self.gravity * delta_Time
        self.pos.y += self.direction * delta_Time
        self.rect.y = round(self.pos.y)

    def player_jump(self):
        self.direction = -400

    def update(self, delta_Time):
        self.player_gravity(delta_Time)