import pygame, sys, time
from pygame import mixer
from gamesettings import *
from homebutton import HomeButton
from gameoverbutton import GameOverButton
from background import Background
from player import Player
from obstacle import Obstacle
from random import randint

class Game():
    def __init__(self):
        pygame.init()
        mixer.init()
        self.screen_Size = pygame.display.set_mode((window_Width, window_Height))
        pygame.display.set_caption('FlappyBird Mock')
        self.clock = pygame.time.Clock()

        # setting the game state
        self.game_State = 'home'

        # setting sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # importing homepage/game over page buttons and background image
        self.start_Btn = pygame.image.load('../images/background/home/start_btn.png').convert_alpha()
        self.exit_Btn = pygame.image.load('../images/background/home/exit_btn.png').convert_alpha()
        self.home_Bg = pygame.image.load('../images/background/home/background.jpg').convert()
        self.home_Bg_Rect = self.home_Bg.get_rect(topleft = (0, 0))

        # creating the button instance for the homepage
        self.start_Button = HomeButton(window_Width / 2, window_Height * 2/5, self.start_Btn, self.screen_Size, 0.9)
        self.exit_Button = HomeButton(window_Width / 2, window_Height * 3/5, self.exit_Btn, self.screen_Size, 0.9)

        # importing game over image for the game over page
        game_Over_Img = pygame.image.load('../images/background/done/game_over.jpg').convert()
        width = game_Over_Img.get_width()
        height = game_Over_Img.get_height()
        self.game_Over_Img_Scaled = pygame.transform.scale(game_Over_Img, (int(width * 0.6), int(height * 0.6)))
        self.game_Over_Img_Rect = self.game_Over_Img_Scaled.get_rect(midtop = (window_Width / 2, window_Height / 10))

        # creating the button instance for the game over page
        self.start_Button = GameOverButton(window_Width / 2, window_Height * 3/5, self.start_Btn, self.screen_Size, 0.9)
        self.exit_Button = GameOverButton(window_Width / 2, window_Height * 4/5, self.exit_Btn, self.screen_Size, 0.9)

        # creating the score to be displayed on the game over page
        self.score = 0
        self.score_Offset = 0
        self.text_Font = pygame.font.Font('../font/Pixeltype.ttf', 50)

        # importing the background image for the play page and calculating the scaling factor
        bkg_Height = pygame.image.load('../images/background/game/background.jpg').get_height()
        self.scaling = window_Height / bkg_Height

        # sprite setup
        Background(self.all_sprites, self.scaling)
        self.player = Player(self.all_sprites, self.scaling / 25)

        # setting up the obstacle timer
        self.pipe_Frequency = 1500
        self.obstacle_Timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_Timer, self.pipe_Frequency)


        # playing background music
        mixer.music.load('../music/background_music.mp3')
        mixer.music.play(-1)

        # import game over sound effect
        self.game_Over_Sound = pygame.mixer.Sound('../music/dead.wav')

    def home(self):
        while self.game_State == 'home':

            # setting the background
            self.screen_Size.blit(self.home_Bg, self.home_Bg_Rect)

            # the game will start playing when the user pressed the start button
            if self.start_Button.draw():
                self.game_State = 'play'
                self.score_Offset = pygame.time.get_ticks()
                self.play()
                
            # program will terminate if the user pressed the exit button
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

    def game_over(self):
        while self.game_State == 'game_over':

            # displaying the images and buttons and score achieved for the current game
            self.screen_Size.fill('Black')
            self.score_Text = self.text_Font.render(f' Your Score: {self.score}', False, 'White')   
            self.score_Text_Rect = self.score_Text.get_rect(midtop = (window_Width / 2, window_Height * 2/5))
            self.screen_Size.blit(self.game_Over_Img_Scaled, self.game_Over_Img_Rect)
            self.screen_Size.blit(self.score_Text, self.score_Text_Rect)

            # the game will start playing when the user pressed the start button
            if self.start_Button.draw():
                self.game_State = 'play'
                self.score_Offset = pygame.time.get_ticks()

                self.player = Player(self.all_sprites, self.scaling / 25)
                
            # program will terminate if the user pressed the exit button
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

    def display_pipe(self):
        pipe_Offset_Lower = randint(50, 100)
        pipe_Offset_Upper = randint(400, 500)
        if 10 < self.score < 20:
            pipe_Offset_Lower = randint(50, 100)
            pipe_Offset_Upper = randint(200, 300)

        if self.score > 20:
            pipe_Offset_Lower = randint(80, 100)
            pipe_Offset_Upper = randint(200, 250)
        self.up_Pipe = Obstacle([self.all_sprites, self.collision_sprites], self.scaling, 'up', pipe_Offset_Lower, pipe_Offset_Upper)
        self.down_Pipe = Obstacle([self.all_sprites, self.collision_sprites], self.scaling, 'down', pipe_Offset_Lower, pipe_Offset_Upper)

    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.collision_sprites, False, pygame.sprite.collide_mask) or self.player.rect.top <= 0 or self.player.rect.bottom >= window_Height:
            self.player.kill()
            self.game_State = 'game_over'

            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_Type == 'pipe':
                    sprite.kill()

            # play game over sound effect
            self.game_Over_Sound.play()

            self.game_State = 'game_over'
            self.game_over()

    def display_score(self):
        if self.game_State == 'play':
            # using the time the game has been running as the score
            self.score = (pygame.time.get_ticks() - self.score_Offset) // 1000
            score_Pos = window_Height / 10

        # setting the styling and the location to put the score
        score_Text = self.text_Font.render(f'{self.score}', False, 'White')
        score_Rect = score_Text.get_rect(midtop = (window_Width / 2, score_Pos))
        self.screen_Size.blit(score_Text, score_Rect)

    def play(self):
        last_time = time.time()

        while self.game_State == 'play':

            # creating the delta time
            delta_Time = time.time() - last_time
            last_time = time.time()

            # checks the events while game is running
            for event in pygame.event.get():

                # closes the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # checks if the user pressed the space key to jump
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.player.player_jump()

                if self.pipe_Frequency > 500:
                    self.pipe_Frequency -= 100
                pygame.time.set_timer(self.obstacle_Timer, self.pipe_Frequency)
                # prints a pipe on the screen everytime the timer is activated
                if event.type == self.obstacle_Timer:
                    self.display_pipe()

            self.player.draw(self.screen_Size)
            self.all_sprites.update(delta_Time)
            self.all_sprites.draw(self.screen_Size)

            self.player_collision()
            self.display_score()

            pygame.display.update()
            self.clock.tick(FPS)

    # def run(self):
        while True:
            if self.game_State == 'home':
                self.game_State = self.home()

            if self.game_State == 'play':
                self.play()

            if self.game_State == 'game_over':
                self.game_over()

            # checks the events while game is running
            for event in pygame.event.get():

                # closes the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
if __name__ == '__main__':
    game = Game()
    game.home()
