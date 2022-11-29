import pygame

class GameOverButton():
    def __init__(self, x, y, image, screen, scale):
        """
        Constructor for the GameOverButton class

        Args:
            x: x position of the button
            y: y position of the button
            image: the image of the button
            screen: the screen size of the button
            scale: the scale factor of the image

        Returns:
            None
        """

        # gets the width and height of the image
        width = image.get_width()
        height = image.get_height()

        # scales the image
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.screen_Size = screen
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)
        self.mouse_Clicked = False

    def draw(self):
        """
        Draws the button

        Description:
            Draws the button and checks if the button was pressed or not

        Args:
            None

        Returns:
            True if the button was pressed
            False if the button was not pressed
        """
        # checks if the user clicked on a button
        mouse_Pos = pygame.mouse.get_pos()
        pressed = False

        # check if the mouse is clicked or not
        if self.rect.collidepoint(mouse_Pos):
            if pygame.mouse.get_pressed()[0] == True and self.mouse_Clicked == False:
                self.mouse_Clicked = True
                pressed = True           

            # resets the click state
            if pygame.mouse.get_pressed()[0] == False:
                self.mouse_Clicked = False

        # displays the buttons on the homepage
        self.screen_Size.blit(self.image, (self.rect.x, self.rect.y))

        return pressed

    