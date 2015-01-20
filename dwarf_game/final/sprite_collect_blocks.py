# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://programarcadegames.com/
# http://simpson.edu/computer-science/

# Explanation video: http://youtu.be/4W2AqUetBi4

import random
import pygame
import sc_block
import goodblock
import badblock
import player

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
red      = ( 255,   0,   0)
blue     = (   0,   0, 255)
green    = (   0, 255,   0)

#Load sounds

pygame.mixer.init()
screen_edge_sound = pygame.mixer.Sound("jumpland.wav")
good_block_sound = pygame.mixer.Sound("healspell1.wav")
bad_block_sound = pygame.mixer.Sound("bad_block.wav")


# Initialize Pygame
pygame.init()

# Set the height and width of the screen
screen_width = 1600
screen_height = 800
screen = pygame.display.set_mode([screen_width,screen_height])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
good_block_list = pygame.sprite.Group()
bad_block_list = pygame.sprite.Group()

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

for i in range(50):
    # This represents a block
    
    block = goodblock.GoodBlock("Shroom_Small.png")

    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height)
    
    # Add the block to the list of objects
    good_block_list.add(block)
    all_sprites_list.add(block)

for i in range(50):
    # This represents a block
    block = badblock.BadBlock("Shroom.png")

    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height)
    
    # Add the block to the list of objects
    bad_block_list.add(block)
    all_sprites_list.add(block)

# Create a red player block
player = player.Player("Dwarf_Miner.png",800, 400)
all_sprites_list.add(player)

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0

# -------- Main Program Loop -----------

while done==False:
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
    player.update()   
    
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

pygame.quit()
