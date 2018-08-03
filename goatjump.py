"""
Pygame base template for opening a window, done with functions
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
"""
 
import pygame
import random
import level
import sprites
from constants import *


def main():
    
    """ Main function for the game. """
    pygame.init()
 
    # Set the width and height of the screen [width,height]
    size = [VIEW_WIDTH, VIEW_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("GoatJump")
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    processing = "Nothing"

    goat = sprites.Goat()
    level_1 = level.Level()
   
    # -------- Main Program Loop -----------
    while not done:
        
        # Event Processing
        done = process_events(goat)
                
        # Game Logic
        goat.update(level_1)
            
        # Drawing
        screen.fill(WHITE)

        level_1.render(screen)
        goat.render(screen, level_1.view)
         
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
        # Limit to 60 frames per second
        clock.tick(FRAMES_PER_SECOND)
        
 
    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()
    
def process_events(goat):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # handle left 
                processing = "K_LEFT => DOWN"
                
            elif event.key == pygame.K_RIGHT:
                # handle right 
                processing = "K_RIGHT => DOWN"
                
            elif event.key == pygame.K_UP:
                # handle up 
                processing = "K_UP => DOWN"
                
            elif event.key == pygame.K_DOWN:
                # handle down
                processing = "K_DOWN => DOWN"
                
            elif event.key == pygame.K_SPACE:
                processing = "K_SPACE => DOWN"
                goat.do_actionkey_down()
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                # handle left 
                processing = "K_LEFT => UP"
            elif event.key == pygame.K_RIGHT:
                # handle right 
                processing = "K_RIGHT => UP"
            elif event.key == pygame.K_UP:
                # handle up 
                processing = "K_UP => UP"
            elif event.key == pygame.K_DOWN:
                # handle down
                processing = "K_DOWN => UP"
                
        return False

 
if __name__ == "__main__":
    main()
