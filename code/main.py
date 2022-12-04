import pygame, sys, time, requests, json, datetime 
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
        """
        Constructor

        Sets up the entire game 

        Args: None

        Returns: None
        """
        pygame.init()
        mixer.init()
        self.screen_Size = pygame.display.set_mode((window_Width, window_Height))
        pygame.display.set_caption('Kirby Bird')
        self.clock = pygame.time.Clock()

        # setting the game state
        self.game_State = 'login'
        self.play_Game = False

        # setting sprite groups
        self.background_sprite = pygame.sprite.Group()
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
        self.background = Background(self.background_sprite, self.scaling)
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
        self.user_Submit = False


                    
    def submit_Score(self):
        """
        Method to submit the score

        Description:
        Sends a post request to the website and passes a dictionary for the API to read and save

        Args: None

        Returns: 
            prints to the console if the post request was not successful
        """

        try:
            # url to the website
            url = 'http://127.0.0.1:5000/submitscore'

            # getting the current date and time info
            dateInfo = datetime.datetime.now()
            date = f"{dateInfo.month}-{dateInfo.day}-{dateInfo.year} {dateInfo.hour}:{dateInfo.minute}"

            # creating the json object ot send as a POST request
            dict = {
                "username": self.username,
                "score": self.score,
                "date": date
            }

            # send the post request to the website
            requests.post(url, json = dict)

        except:
            print('didnt work')

    def home(self):
        """
        Method to display the home page

        Description:
        Displays the home page after the login screen

        Interaction:
        Start button: starts the game
        Exit button: exits the game

        Args: None

        Returns: None
        """
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
        """
        Method to display the game over screen

        Description:
        Displays the game over screen with the score achieved and the option to submit the score to the website

        Interaction:
        Start button: starts the game
        Exit button: exits the game

        Args: None

        Returns: None
        """
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
                input_Notes_Font = pygame.font.Font('../font/Pixeltype.ttf', 35)

                # user input instructions
                input_Notes_Surface = input_Notes_Font.render('Press "Enter" to submit score', False, 'white')
                input_Notes_Rect = input_Notes_Surface.get_rect(midtop = (window_Width / 2, window_Height * 5/12))

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
                self.score = 0
                self.game_State = 'play'
                self.play_Game = False

                self.player = Player(self.all_sprites, self.scaling / 25)
                
            # program will terminate if the user pressed the exit button
            if self.exit_Button.draw():
                pygame.quit()
                sys.exit()

            # checks the events while game is running
            for event in pygame.event.get():

                # submits the user score achieved to the website
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.user_Submit = True
                    self.submit_Score()

                # closes the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    def display_pipe(self):
        """
        Method to display the pipe

        Description:
        Calculates the pipe offset depending on the score the user achieved which is time dependant 

        Args: None

        Returns: None
        """
        # setting the center point of the pipes
        center_Point = int(window_Height / 2)
        up_Down = choice(('up', 'down'))

        # setting the offset value from the center point
        if 0 <= self.score < 10:
            pipe_Offset = int(randint(225, 250) / 2)
            if up_Down == 'up':
                center_Point += int(randint(50, 100))
            else:
                center_Point -= int(randint(50, 100))

        elif 10 <= self.score <= 20:
            pipe_Offset = int(randint(200, 225) / 2)
            if up_Down == 'up':
                center_Point += int(randint(100, 150))
            else:
                center_Point -= int(randint(100, 150))

        elif self.score > 20:
            pipe_Offset = int(randint(180, 200) / 2)
            if up_Down == 'up':
                center_Point += int(randint(150, 200))
            else:
                center_Point -= int(randint(150, 200))

        pipe_Start = window_Width + (window_Width / 15)

        self.up_Pipe = Obstacle([self.all_sprites, self.collision_sprites], self.scaling, 'up', center_Point, pipe_Start, pipe_Offset)
        self.down_Pipe = Obstacle([self.all_sprites, self.collision_sprites], self.scaling, 'down', center_Point, pipe_Start, pipe_Offset)

    def player_collision(self):
        """
        Method to check the player collision

        Description:
        Checks if the player collided with the pipe or the top or the bottom of the screen

        Args: None

        Returns: None
        """
        # checks if the player has collided
        if pygame.sprite.spritecollide(self.player, self.collision_sprites, False, pygame.sprite.collide_mask) or self.player.rect.top <= 0 or self.player.rect.bottom >= window_Height:
            
            # deletes the player
            self.player.kill()
            self.game_State = 'game_over'

            for sprite in self.collision_sprites.sprites():
                # deleted all collision sprites
                sprite.kill()

            # play game over sound effect
            self.game_Over_Sound.play()
            self.game_State = 'game_over'
            self.user_Submit = False
            self.game_over()

    def display_score(self):
        """
        Method to display the score

        Description:
        Displays the score depending on the score the user achieved which is time dependant

        Args: None

        Returns: None
        """
        if self.game_State == 'play':
            # using the time the game has been running as the score
            self.score = (pygame.time.get_ticks() - self.score_Offset) // 1000
            score_Pos = window_Height / 10

        # setting the styling and the location to put the score
        score_Text = self.text_Font.render(f'{self.score}', False, 'White')
        score_Rect = score_Text.get_rect(midtop = (window_Width / 2, score_Pos))
        self.screen_Size.blit(score_Text, score_Rect)

    def play(self):
        """
        Method to play the game

        Description:
        Plays the game and calls required classes to update its positions on the screen

        Args: None

        Returns: None
        """
        last_time = time.time()

        while self.game_State == 'play':

            # creating the delta time
            delta_Time = time.time() - last_time
            last_time = time.time()

            self.background_sprite.update(delta_Time)
            self.background_sprite.draw(self.screen_Size)
            self.player.draw(self.screen_Size)

            # checks the events while game is running
            for event in pygame.event.get():

                if self.play_Game == False:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.score_Offset = pygame.time.get_ticks()
                        self.play_Game = True
                        self.score = 0


                if self.play_Game == True:
                    # checks if the user pressed the space key to jump
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.player.player_jump()

                    # spawns the pipes
                    if event.type == self.obstacle_Timer:
                        self.display_pipe()

                        # increases the pipe spawn frequency
                        if self.pipe_Frequency > 800:
                            self.pipe_Frequency -= 25

                # closes the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.play_Game == True:
                self.all_sprites.draw(self.screen_Size)
                self.player_collision()
                self.all_sprites.update(delta_Time)
                self.display_score()
            
            pygame.display.update()
            self.clock.tick(FPS)

    def checkUser(self, username, password):
        """
        Method to check if the user is valid

        Description:
        Checks if the username and password is in the database and if not, it adds it to the database

        Args:
            username (str): Username of the user
            password (str): Password of the user
        """
        # reads the database file
        with open('../database/users.json', 'r') as readFile:
            user_List = json.load(readFile)

            # checks if there is a matching username and password in the database
            for user in user_List:
                if user["username"] == username and user["password"] == password:
                    self.valid = 'True'

            if self.valid != 'True':
                self.valid = 'False-Attempt'
        
    def loginPage(self):
        """
        Method to login or sign the user up

        Description:
        This method will display the login page and takes in the username and password inputted by the user

        Args: None

        Returns: None
        """

        # loginPage user inputs
        self.arrow = '>'
        self.input_Box = 'username'
        self.valid = 'False' # False: Has not attempted login, True: Login exists, False-Attempt: attempted login but failed

        self.username_Label = 'Username:'
        self.username = ''

        self.password_Label = 'Password:'
        self.password = ''

        arrow_yPos = window_Height * 5/16 

        while self.game_State == 'login':
            # setting the x position
            x = window_Width * 1/6

            # setting the background
            self.screen_Size.blit(self.home_Bg, self.home_Bg_Rect)

            # # setting the font for the text input
            input_Text_Font = pygame.font.Font('../font/Pixeltype.ttf', 40)
            arrow_Text_Font = pygame.font.Font('../font/Pixeltype.ttf', 70)

            # # setting the username and password input box
            username_Label_Surface = input_Text_Font.render(self.username_Label, False, 'white')
            username_Input = input_Text_Font.render(self.username, False, 'white')

            password_Label_Surface = input_Text_Font.render(self.password_Label, False, 'white')
            password_Input = input_Text_Font.render(self.password, False, 'white')

            arrow_Surface = arrow_Text_Font.render(self.arrow, False, 'white')

            # # setting the location of the text input box
            username_Label_Rect = username_Label_Surface.get_rect(midleft = (x, window_Height * 4/16))
            username_Input_Rect = username_Input.get_rect(midleft = (x, window_Height * 5/16))

            password_Label_Rect = password_Label_Surface.get_rect(midleft = (x, window_Height * 7/16))
            password_Input_Rect = password_Input.get_rect(midleft = (x, window_Height * 8/16))

            arrow_Rect = arrow_Surface.get_rect(midright = (x - 20, arrow_yPos))

            # # displaying the text on the screen
            self.screen_Size.blit(username_Label_Surface, username_Label_Rect)
            self.screen_Size.blit(username_Input, username_Input_Rect)

            self.screen_Size.blit(password_Label_Surface, password_Label_Rect)
            self.screen_Size.blit(password_Input, password_Input_Rect)

            self.screen_Size.blit(arrow_Surface, arrow_Rect)

            # displays the error message if the user entered an invalid user account
            if self.valid == 'False-Attempt' or self.valid == 'False-Attempt-Notice':

                self.error_Message = 'The username or password is invalid'
                self.error_Surface = input_Text_Font.render(self.error_Message, False, 'red')
                self.error_Rect = self.error_Surface.get_rect(midtop = (window_Width / 2, window_Height * 11/16))
                self.screen_Size.blit(self.error_Surface, self.error_Rect)

            for event in pygame.event.get():

                # exits the game gracefully
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # check if the state is in either username or password input
                if self.input_Box == 'username' and event.type == pygame.KEYDOWN:

                    # if the enter key is pressed then change the input box to the password
                    if event.key == pygame.K_RETURN:
                        self.input_Box = 'password'
                        arrow_yPos = window_Height * 8/16

                    # deletes the last character from the string
                    elif event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        self.username += event.unicode
    
                elif self.input_Box == 'password':
                    if event.type == pygame.KEYDOWN:

                        # if the return key is pressed then navigate to the home page
                        if event.key == pygame.K_RETURN:
                            self.checkUser(self.username, self.password)

                            if self.valid == 'True':
                                self.game_State = 'home'
                                self.home()
                        
                        # deletes a last character from the string
                        elif event.key == pygame.K_BACKSPACE:
                            self.password = self.password[:-1]

                        else:
                            self.password += event.unicode

                    elif self.valid == 'False-Attempt':
                        self.valid = 'False-Attempt-Notice'
                        self.input_Box = 'username'
                        self.username = ''
                        self.password = ''
                        arrow_yPos = window_Height * 5/16

                        # self.loginPage()


            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.loginPage()
