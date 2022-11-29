import pygame
from gamesettings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, scaling):
        """
        Constructor for the Player class

        Description:
            Imports the image of kirby and masks the kirby so that the hit box is around the kirby outline

        Args:
            groups: adds the player to the sprite group
            scaling: determines the scaling for the image of kirby

        Returns: None
        """
        super().__init__(groups)
        self.sprite_Type = 'player'

        # importing image of kirby
        kirby_Img = pygame.image.load('../images/player/kirby1.png').convert_alpha()
        kirby_Img_Scaled = pygame.transform.scale(kirby_Img, pygame.math.Vector2(kirby_Img.get_size()) * scaling)
        self.image = kirby_Img_Scaled
        self.rect = self.image.get_rect(midleft = (window_Width / 20, window_Height / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # setting the player movements
        self.gravity = 600
        self.direction = 0

        # setting the mask for the player
        self.mask = pygame.mask.from_surface(self.image)

        # importing the jump sound effect
        self.jump_Sound = pygame.mixer.Sound('../music/jump.wav')

    def draw(self, screen_Size):
        """
        Draws the player sprite

        Args:
            screen_Size: size of the screen

        Returns: None
        """
        screen_Size.blit(self.image, self.rect)

    def player_gravity(self, delta_Time):
        """
        Applies gravity to the player

        Description:
            Applies gravity to the player and increases gradually as the player continuously falls down

        Args:
            delta_Time: time difference between the last frame and the current frame

        Returns: None
        """
        self.direction += self.gravity * delta_Time
        self.pos.y += self.direction * delta_Time
        self.rect.y = round(self.pos.y)

    def player_jump(self):
        """
        Jumps the player

        Description:
            Jumps the player

        Args: None

        Returns: None
        """
        self.direction = -360
        self.jump_Sound.play()

    def update(self, delta_Time):
        """
        Updates the player

        Description:
            Updates the player movement

        Args:
            delta_Time: time difference between the last frame and the current frame

        Returns: None
        """
        self.player_gravity(delta_Time)