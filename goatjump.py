"""
Pygame base template for opening a window, done with functions
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
"""
 
import pygame
import random
import sprites
from constants import *


def main():
    
    """ Main function for the game. """
    pygame.init()
 
    # Set the width and height of the screen [width,height]
    size = [700, 500]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("My Game")
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    processing = "Nothing"

    # indicator states: clear, power, direction, cleanup
    indicator = sprites.Indicator()
    
    
    # -------- Main Program Loop -----------
    while not done:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
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
                    indicator.do_actionkey_down()
                    
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
                #elif event.key == pygame.K_SPACE:
                    #do_spacekey_up()

                
        # Event Processing
 
        # Game Logic
        indicator.update()
            
        # Drawing
        screen.fill(WHITE)

        indicator.render(screen)
         
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
        # Limit to 60 frames per second
        clock.tick(60)
        
 
    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()
 
if __name__ == "__main__":
    main()
