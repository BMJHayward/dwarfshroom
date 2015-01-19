#!/usr/bin/python
""" Client-side form of dwarf-mushroom game. Refactored with call backs to
transpile to Javascript.
"""
# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://programarcadegames.com/
# http://simpson.edu/computer-science/

# Explanation video: http://youtu.be/4W2AqUetBi4

import random, os.path
import os, sys
try:
    import pygame
    from pygame.locals import *
    from pygame.compat import geterror
    engine = 'pygame'
except ImportError:
    import pyjsdl as pygame
    from pyjsdl.locals import * 
    pygame.sprite.RenderPlain = pygame.sprite.Group
    engine = 'pyjsdl'

# To control main game loop
done = False

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
red      = ( 255,   0,   0)
blue     = (   0,   0, 255)
green    = (   0, 255,   0)

Rect = pygame.Rect
Color = pygame.Color
SCREENRECT = Rect(0, 0, 540, 480) # """Need to increase this later, or make it dynamic to viewport"""
# Could use this: SCREENRECT = Rect(0, 0, 1600, 800)
score = 0

# Set the height and width of the screen
screen_width = 1600
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
good_block_list = pygame.sprite.Group()
bad_block_list = pygame.sprite.Group()

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

if engine == 'pygame':
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, 'data')
elif engine == 'pyjsdl':
    main_dir = ''
    data_dir = os.path.join(main_dir, 'data')

def load_image(filename):

    """loads image to prepare for play"""
    filename = filename.split('.')[0] + '.png'
    filename = os.path.join(main_dir, data_dir, filename)

    try:
        surface = pygame.image.load(filename)
    except pygame.error:
        raise SystemExit('Could not load image {0} {1}'.format(filename, pygame.get_error()))

    return surface.convert_alpha()

def load_images(*files):
    """ loads an array of images"""
    imgs = []
    for filename in files:
        imgs.append(load_image(filename))

    return imgs

class dummysound:
    
    def play(self):
        pass

def load_sound(filename):
    """loads sounds, used in setup"""
    if not pygame.mixer:
        return dummysound()
    filename = os.path.join(main_dir, data_dir, filename)

    try:
        sound = pygame.mixer.Sound(filename)
        return sound
    except pygame.error:
        print'Warning, unable to load, %s' % filename

    return dummysound()

class Player(pygame.sprite.Sprite):
    """ basic player class """
    # -- Attributes
    # Set speed vector
    change_x = 0
    change_y = 0

    # -- Methods
    # Constructor function
    def __init__(self, filename, x, y):
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
    def changespeed(self, x, y):

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

# This class represents the mushrooms        
# It derives from the "Sprite" class in Pygame
class Block(pygame.sprite.Sprite):
    """ used as base for mushrooms. could be used as other non-player objects"""
    # Constructor. Pass in the color of the block, 
    # and its x and y position
    def __init__(self, filename):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        #fullname = os.path.join(self, filename)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(white)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

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

class GoodBlock(Block):

    '''change_x = random.randrange(-1,2)
       change_y = random.randrange(-1,2)
       rect.x += change_x
       rect.y += change_y
    '''
    def __init__(self,filename):
    # Call the parent class (Sprite) constructor
        Block.__init__(self, filename)


class BadBlock(Block):
    
    '''change_x = random.randrange(-1,2)
       change_y = random.randrange(-1,2)  
       rect.x += change_x
       rect.y += change_y    
    '''
    def __init__(self,filename):
    # Call the parent class (Sprite) constructor
        Block.__init__(self, filename)

""" globals: needed for display.setup callback function """
screen = background = clock = screen_edge_sound = good_block_sound = bad_block_sound = None
player = good_mush = bad_mush = all = None
keystate = {K_RIGHT : False, K_LEFT : False, K_SPACE : False}
restart = waiting = False

def wait():
    global waiting

    if not waiting:
        waiting = True
        pygame.time.wait(1000)
    else:
        waiting = False
        pygame.event.clear()
        for key in keystate:
            keystate[key] = False
        if engine == 'pyjsdl':
            pygame.display.setup(run)

def setup():
    global screen
    pygame.init()
    pygame.mixer.init()

    if pygame.mixer and not pygame.mixer.get_init():
        print('Warning, no sound')
        pygame.mixer = None

    screen = pygame.display.set_mode(SCREENRECT.size)

    return screen

def prerun():

    global background, player, all, clock, screen_edge_sound, good_block_sound, bad_block_sound
    #Load sounds
    screen_edge_sound = load_sound("jumpland.wav")
    good_block_sound = load_sound("healspell1.wav")
    bad_block_sound = load_sound("bad_block.wav")
    for i in range(50):
        # This represents a block
        
        block = GoodBlock("data/Shroom_Small.png")

        # Set a random location for the block
        block.rect.x = random.randrange(screen_width)
        block.rect.y = random.randrange(screen_height)
        
        # Add the block to the list of objects
        good_block_list.add(block)
        all_sprites_list.add(block)

    for i in range(50):
        # This represents a block
        block = BadBlock("data/Shroom.png")

        # Set a random location for the block
        block.rect.x = random.randrange(screen_width)
        block.rect.y = random.randrange(screen_height)
        
        # Add the block to the list of objects
        bad_block_list.add(block)
        all_sprites_list.add(block)

    # Create a red player block
    player = Player("data/Dwarf_Miner.png", 270, 240)
    all_sprites_list.add(player)

    #Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    score = 0
    if engine == 'pyjsdl':
        pygame.display.setup(run)

def run():
    global score
    # -------- Main Program Loop -----------
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

            # Set the speed based on the key pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-1,0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(1,0)
            elif event.key == pygame.K_UP:
                player.changespeed(0,-1)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0,1)
                    
        # Reset speed when key goes up      
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(1,0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-1,0)
            elif event.key == pygame.K_UP:
                player.changespeed(0,1)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0,-1)
                    
    #calc speed based on input    
    #player.changespeed()    
    
    # This moves the player block based on the current speed
    #player.update() #comment out to test next update()

    #Updates every sprite
    all_sprites_list.update()
    # Clear the screen
    screen.fill(white)

    # Get the current mouse position. This returns the position
    # as a list of two numbers.
    #pos = pygame.mouse.get_pos()
        
    # Fetch the x and y out of the list, 
       # just like we'd fetch letters out of a string.
    # Set the player object to the mouse location
    #player.rect.x = pos[0]
    #player.rect.y = pos[1]
        
    # See if the player block has collided with anything.
    good_blocks_hit_list = pygame.sprite.spritecollide(player, good_block_list, True)
    # Check the list of collisions.
    for block in good_blocks_hit_list:
        score +=1
        good_block_sound.play()

    #See if the player block has collided with anything.
    bad_blocks_hit_list = pygame.sprite.spritecollide(player, bad_block_list, True)  
    # Check the list of collisions.
    for block in bad_blocks_hit_list:
        score +=-1
        bad_block_sound.play()

    # Select the font to use. Default font, 25 pt size.
    font = pygame.font.Font(None, 25)
         
    # Render the text. "True" means anti-aliased text. 
    text = font.render(str(score), True, black)
         
    # Put the image of the text on the screen at 250x250
    screen.blit(text, [player.rect.x,player.rect.y +35])          
    # Draw all the spites
    all_sprites_list.draw(screen)
        
    # Limit to 20 frames per second
    #clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()


def main():

    global screen
    global done
    screen = setup()

    if engine == 'pygame':
        prerun()
        while done == False:
            run()
        pygame.quit()

    elif engine == 'pyjsdl':
        images = ['./data/Dwarf_miner.png', './data/Shroom.png', './data/Shroom_Small.png']
        pygame.display.setup(prerun, images)

if __name__ == '__main__': 
    main()
