import pygame, sys, time
import json
import requests
from pygame import mixer
from gamesettings import *
from homebutton import HomeButton
from gameoverbutton import GameOverButton
from background import Background
from player import Player
from obstacle import Obstacle
from random import randint, choice

class Game():
    def __init__(self):
        pygame.init()
        mixer.init()
        self.screen_Size = pygame.display.set_mode((window_Width, window_Height))
        pygame.display.set_caption('FlappyBird Mock')
        self.clock = pygame.time.Clock()

        # setting the game state
        self.game_State = 'home'
        self.play_Game = False

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
        self.game_Over_Img_Rect = self.game_Over_Img_Scaled.get_rect(midtop = (window_Width / 2, window_Height / 12))

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

        # enabling user text input when game is over
        self.user_Text = ''
        self.user_Text_Label = 'Username: '
        self.user_Submit = False

    def save_Score(self):

        try:
            url = 'http://127.0.0.1:5000/submitscore'
            dict = {
                "username": "sora",
                "score": 10
            }
            requests.post(url, json = dict)
        except:
            print('didnt work')

        # # read the contents of the scores.json file
        # with open('../database/scores.json', 'r') as readFile:
        #     score_List = json.load(readFile)

        # # creating the instance of the user score
        # user_Score = {
        #     "username": self.user_Text,
        #     "score": self.score
        # }
        
        # # adds the score to the score list
        # score_List.append(user_Score)
        
        # # writes the new score that was added to the database
        # with open('../database/scores.json', 'w') as writeFile:
        #     json.dump(score_List, writeFile)


    def home(self):
        while self.game_State == 'home':

            # setting the background
            self.screen_Size.blit(self.home_Bg, self.home_Bg_Rect)

            # adding the image of kirby on the home screen
            home_Kirby_Img = pygame.image.load('../images/background/home/kirby2.png')
            home_Kirby_Img_Scaled = pygame.transform.scale(home_Kirby_Img, (int(home_Kirby_Img.get_width() / 2), int(home_Kirby_Img.get_height() / 2)))
            home_Kirby_Rect = home_Kirby_Img_Scaled.get_rect(midtop = (window_Width / 2, window_Height / 3))
            self.screen_Size.blit(home_Kirby_Img_Scaled, home_Kirby_Rect)

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
            self.score_Text_Rect = self.score_Text.get_rect(midtop = (window_Width / 2, window_Height * 4/12))
            self.screen_Size.blit(self.game_Over_Img_Scaled, self.game_Over_Img_Rect)
            self.screen_Size.blit(self.score_Text, self.score_Text_Rect)

            # checks if the usr submitted a score or not
            if self.user_Submit == False:
                # setting up the user input box to submit a username
                user_Text_Font = pygame.font.Font('../font/Pixeltype.ttf', 40)
                input_Notes_Font = pygame.font.Font('../font/Pixeltype.ttf', 35)

                # user input instructions
                input_Notes = 'Type your username and press "Enter"'
                input_Notes_Surface = input_Notes_Font.render(input_Notes, False, 'white')
                input_Notes_Rect = input_Notes_Surface.get_rect(midtop = (window_Width / 2, window_Height * 5/12))

                # user input and the label
                user_Text_Surface = user_Text_Font.render(self.user_Text, False, 'white')
                user_Text_Label_Surface = user_Text_Font.render(self.user_Text_Label, False, 'white')

                # setting the location to put the text box on the screen
                user_Text_Rect = user_Text_Surface.get_rect(midleft = (window_Width * 2/5, window_Height * 6/12))
                user_Text_Label_Rect = user_Text_Label_Surface.get_rect(midleft = (window_Width * 1/8, window_Height * 6/12))

                self.screen_Size.blit(user_Text_Surface, user_Text_Rect)
                self.screen_Size.blit(user_Text_Label_Surface, user_Text_Label_Rect)
                self.screen_Size.blit(input_Notes_Surface, input_Notes_Rect)
            
            # displays the "submitted" text if the user has submitted
            else:
                
                # lets the user know that the score was submitted
                input_Notes_Font = pygame.font.Font('../font/Pixeltype.ttf', 40)
                submit_Text = input_Notes_Font.render('Score submitted', False, 'white')
                submit_Text_Rect = submit_Text.get_rect(midtop = (window_Width / 2, window_Height * 6/12))

                self.screen_Size.blit(submit_Text, submit_Text_Rect)

            # the game will start playing when the user pressed the start button
            if self.start_Button.draw():
                self.user_Submit = False
                self.score = 0
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

                # checks if the user enters a username to submit their score
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE and not self.user_Submit:
                        self.user_Text = self.user_Text[:-1]
                    elif len(self.user_Text) > 15:
                        self.user_Text = self.user_Text
                    elif event.key == pygame.K_RETURN and not self.user_Submit:
                        self.user_Submit = True
                        self.save_Score()
                    elif not self.user_Submit:
                        self.user_Text += event.unicode


            pygame.display.update()

    def display_pipe(self):
        # setting the center point of the pipes
        center_Point = int(window_Height / 2)
        up_Down = choice(('up', 'down'))

        # setting the offset value from the center point
        if 0 <= self.score < 10:
            pipe_Offset = int(randint(225, 250) / 2)
            if up_Down == 'up':
                center_Point += int(randint(100, 150))
            else:
                center_Point -= int(randint(100, 150))

        if 10 <= self.score <= 20:
            pipe_Offset = int(randint(200, 225) / 2)
            if up_Down == 'up':
                center_Point += int(randint(100, 150))
            else:
                center_Point -= int(randint(100, 150))

        if self.score > 20:
            pipe_Offset = int(randint(180, 200) / 2)

            if up_Down == 'up':
                center_Point += int(randint(150, 200))
            else:
                center_Point -= int(randint(150, 200))

        pipe_Start = window_Width + (window_Width / 20)

        self.up_Pipe = Obstacle([self.all_sprites, self.collision_sprites], self.scaling, 'up', self.score, center_Point, pipe_Start, pipe_Offset)
        self.down_Pipe = Obstacle([self.all_sprites, self.collision_sprites], self.scaling, 'down', self.score, center_Point, pipe_Start, pipe_Offset)

    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.collision_sprites, False, pygame.sprite.collide_mask) or self.player.rect.top <= 0 or self.player.rect.bottom >= window_Height:
            self.player.kill()
            self.game_State = 'game_over'

            for sprite in self.collision_sprites.sprites():
                sprite.kill()

            # play game over sound effect
            self.game_Over_Sound.play()
            self.game_State = 'game_over'
            self.user_Submit = False
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

                if self.pipe_Frequency > 800:
                    self.pipe_Frequency -= 25

                pygame.time.set_timer(self.obstacle_Timer, self.pipe_Frequency)

                # prints a pipe on the screen everytime the timer is activated
                if event.type == self.obstacle_Timer:
                    self.display_pipe()
            
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
