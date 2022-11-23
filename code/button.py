import pygame

class Button():
    def __init__(self, x, y, image, screen, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.screen_Size = screen
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)
        self.mouse_Clicked = False

    def draw(self):
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

    