import pygame
from gamesettings import *

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups, scaling, position, center_Point, pipe_Start, pipe_Offset):
        """
        Constructor for the obstacle class

        Args:
            groups: to set the sprite group
            scaling: scale the image
            position: checking if the pipe is upright or down
            center_Point: assigns the center point to start the offset, y coordinate
            pipe_Start: starting point, x coordinate for the pipe (starts off screen)
            pipe_Offset: a random value that determines the offset from the center point

        Returns: None
        """
        super().__init__(groups)
        self.sprite_Type = 'pipe'

        # loads the background image and scales it to fit the screen
        pipe_Img = pygame.image.load('../images/background/game/pipe.png').convert_alpha()
        self.image = pygame.transform.scale(pipe_Img, pygame.math.Vector2(pipe_Img.get_size()) * scaling)
        self.rect = self.image.get_rect()

        # assigning the offset and starting point of the pipe
        if position == 'up':
            self.rect.midtop = [pipe_Start, center_Point + pipe_Offset]
            self.mask = pygame.mask.from_surface(self.image)
        if position == 'down':
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.midbottom = [pipe_Start, center_Point - pipe_Offset]
            self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta_Time):
        """
        Updates the pipe

        Moves the pipe from right to left and deletes the pipe once it goes off the screen on the left

        Args:
            delta_Time: time passed since last 
            
        Returns: None
        """
        self.rect.x -= 300 * delta_Time
        if self.rect.right <= -100:
            self.kill()



