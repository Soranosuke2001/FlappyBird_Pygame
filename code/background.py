import pygame
from gamesettings import *

class Background(pygame.sprite.Sprite):
    def __init__(self, groups, scaling):
        """
        Constructor for the Background class

        Description:


        Args:
            groups: the sprite group to be added to
            scaling: the scaling factor for the background image

        Returns: None
        """
        super().__init__(groups)

        # importing the background image and scaling it to fit the window size
        bkg_Img = pygame.image.load('../images/background/game/background.jpg').convert()

        # sets the new width and height of the background
        width_Scaled = bkg_Img.get_width() * scaling
        height_Scaled = bkg_Img.get_height() * scaling

        # scales the background image
        bkg_Img_Scaled = pygame.transform.scale(bkg_Img, (width_Scaled, height_Scaled))
        self.image = pygame.Surface((width_Scaled * 2, height_Scaled))

        # displaying the background image on the window, and printing 2 to double the width
        self.image.blit(bkg_Img_Scaled, (0, 0))
        self.image.blit(bkg_Img_Scaled, (width_Scaled, 0))

        self.rect = self.image.get_rect(topleft = (0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)


    def update(self, delta_Time):
        """
        Updates the background image

        Description:
            Moves the background image from right to left continuously

        Args:
            delta_Time: the amount of time passed since the last update
        """

        # moveing the background image from left to right
        self.pos.x -= 300 * delta_Time

        if self.rect.centerx <= 0:
            self.pos.x = 0
        
        self.rect.x = round(self.pos.x)


