import pygame
import random
import sc_block

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
red      = ( 255,   0,   0)
blue     = (   0,   0, 255)
green    = (   0, 255,   0)

screen_width=1600
screen_height=800

pygame.init()

class GoodBlock(sc_block.Block):

    '''change_x = random.randrange(-1,2)
    change_y = random.randrange(-1,2)
    rect.x += change_x
    rect.y += change_y
    '''
    def __init__(self,filename):
    # Call the parent class (Sprite) constructor
        sc_block.Block.__init__(self, filename)
    
    #Create new pos for sprite
    def update(self):
        
        self.change_x = random.randrange(-1,2)
        self.change_y = random.randrange(-1,2)
        self.rect.x += self.change_x
        self.rect.y += self.change_y        
        
        #If statements to prevent walking off screen
        if self.rect.x < 0:
            self.rect.x = 0   
        if self.rect.x > screen_width:
            self.rect.x = screen_width 
        if self.rect.y < 0:
            self.rect.y = 0   
        if self.rect.y > screen_height:
            self.rect.y = screen_height
