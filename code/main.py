import pygame, sys
from gamesettings import *

class Game():
    def __init__(self):
        screen_Size = pygame.display.set_mode((window_Width, window_Height))
        pygame.display.set_caption('FlappyBird Mock')

        # setting the game state
        self.gate_State = 'home'

    def home(self):
        while self.gate_State == 'home':

            # checks the events while game is running
            for event in pygame.event.get():

                # closes the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.home()
