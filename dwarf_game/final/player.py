import pygame
import random

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
red      = ( 255,   0,   0)
blue     = (   0,   0, 255)
green    = (   0, 255,   0)

screen_width=1600
screen_height=800


pygame.init()

screen_edge_sound = pygame.mixer.Sound("jumpland.wav")

# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):

    # -- Attributes
    # Set speed vector
    change_x = 0
    change_y = 0
    
    # -- Methods
    # Constructor function
    def __init__(self,filename,x,y):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(white)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    # Change the speed of the player
    def changespeed(self,x,y):
        self.change_x += x
        self.change_y += y
        
    # Find a new position for the player
    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        
        if self.rect.x < 0:
            self.rect.x = 0
            screen_edge_sound.play()
            
        if self.rect.x > screen_width:
            self.rect.x = screen_width
            screen_edge_sound.play()
            
        if self.rect.y < 0:
            self.rect.y = 0
            screen_edge_sound.play()
            
        if self.rect.y > screen_height:
            self.rect.y = screen_height
            screen_edge_sound.play()