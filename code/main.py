import pygame, sys
from gamesettings import *
from button import Button

class Game():
    def __init__(self):
        self.screen_Size = pygame.display.set_mode((window_Width, window_Height))
        pygame.display.set_caption('FlappyBird Mock')

        # setting the game state
        self.gate_State = 'home'

        # importing homepage buttons and background image
        self.start_Btn = pygame.image.load('../images/background/home/start_btn.png').convert_alpha()
        self.exit_Btn = pygame.image.load('../images/background/home/exit_btn.png').convert_alpha()
        self.home_Bg = pygame.image.load('../images/background/home/background.jpg').convert()

        # creating the button instance
        self.start_Button = Button(window_Width / 2, window_Height * 2/5, self.start_Btn, self.screen_Size, 0.9)
        self.exit_Button = Button(window_Width / 2, window_Height * 3/5, self.exit_Btn, self.screen_Size, 0.9)


    def home(self):
        while self.gate_State == 'home':

            # setting the background
            self.screen_Size.fill((202, 228, 241))

            if self.start_Button.draw():
                print('Start was pressed')
            if self.exit_Button.draw():
                pygame.quit()
                sys.exit()

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
