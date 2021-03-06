#! /usr/bin/env python3

import sys
import pygame
from helpers import *

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

class Settings:
    screenWidth = 800
    screenHeight = 600

class PyManMain:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Settings.screenWidth, Settings.screenHeight))


    def MainLoop(self):
        """This is the Main Loop of the Game"""

        """Load All of our Sprites"""
        self.LoadSprites();

        """tell pygame to keep sending up keystrokes when they are
        held down"""
        pygame.key.set_repeat(10, 30)

        """Create the background"""
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_q:
                        sys.exit()
                    if event.key in (K_RIGHT, K_LEFT, K_UP, K_DOWN, K_w, K_a, K_s, K_d):
                        self.snake.move(event.key)

            """Check for collision"""
            lstCols = pygame.sprite.spritecollide(self.snake, self.pellet_sprites, True)
            """Update the amount of pellets eaten"""
            self.snake.pellets = self.snake.pellets + len(lstCols)
                        
            self.screen.blit(self.background, (0, 0))     
            if pygame.font:
                font = pygame.font.Font(None, 36)
                text = font.render("Pellets %s" % self.snake.pellets, 1, (255, 0, 0))
                textpos = text.get_rect(centerx=self.background.get_width()/2)
                self.screen.blit(text, textpos)
               
            self.pellet_sprites.draw(self.screen)
            self.snake_sprites.draw(self.screen)
            pygame.display.flip()

    def LoadSprites(self):
        """Load the sprites that we need"""
        self.snake = Snake()
        self.snake_sprites = pygame.sprite.RenderPlain((self.snake))

        """figure out how many pellets we can display"""
        nNumHorizontal = int(Settings.screenWidth/64)
        nNumVertical = int(Settings.screenHeight/64)
        """Create the Pellet group"""
        self.pellet_sprites = pygame.sprite.Group()
        """Create all of the pellets and add them to the pellet_sprites group"""
        for x in range(nNumHorizontal):
            for y in range(nNumVertical):
                self.pellet_sprites.add(Pellet(pygame.Rect(x*64, y*64, 64, 64)))        

class Pellet(pygame.sprite.Sprite):
    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self) 
        self.image, self.rect = load_image('pellet2.png',-1)
        if rect != None:
            self.rect = rect

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image, self.rect = load_image('python.png',-1)
        self.pellets = 0
        """Set the number of Pixels to move each time"""
        self.x_dist = 32
        self.y_dist = 32

        self.xMax = Settings.screenWidth - self.rect.width
        self.yMax = Settings.screenHeight - self.rect.height

    def move(self, key):
        """Move your self in one of the 4 directions according to key"""
        """Key is the pyGame define for either up,down,left, or right key
        we will adjust ourselves in that direction"""
        xMove = 0;
        yMove = 0;
        
        if (key == K_RIGHT or key == K_d):
            xMove = self.x_dist
        elif (key == K_LEFT or key == K_a):
            xMove = -self.x_dist
        elif (key == K_UP or key == K_w):
            yMove = -self.y_dist
        elif (key == K_DOWN or key == K_s):
            yMove = self.y_dist

        if self.rect.x + xMove < 0: xMove = 0
        if self.rect.y + yMove < 0: yMove = 0
        if self.rect.x + xMove > self.xMax: xMove = 0
        if self.rect.y + yMove > self.yMax: yMove = 0
        self.rect.move_ip(xMove,yMove);

if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()
