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


class Game():
    
    def __init__(self):
        self.lobby = True
        self.lobby_message = "Get Ready! SPACEBAR to start..."
        self.goat = sprites.Goat("pregame")
        self.level = level.Level()
    
    def process_events(self):
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
                    if self.lobby == True:
                        if self.goat.jumpstate == "deaded":
                            # New goat and level
                            self.goat = sprites.Goat("midair")
                            self.level = level.Level()
                        elif self.goat.jumpstate == "pregame":
                            self.goat.jumpstate = "midair"
                            
                        self.lobby = False
                    else:
                        self.goat.do_actionkey_down()
                    
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
        
        
    def update(self):
        self.goat.update(self.level)
        if self.goat.jumpstate == 'deaded':
            self.lobby = True
            self.lobby_message = "You died :(  SPACEBAR to try again"
    
    
    def render(self, screen):
         
        screen.fill(BLACK)

        self.level.render(screen)
        self.goat.render(screen, self.level.view)
        
        if self.lobby == True:
            message_box(screen, self.lobby_message)
        

def message_box(screen, message, frame_top = 100, frame_left = 0):
    
    frame_top = 100
    font = pygame.font.SysFont('Courier New', FONT_SIZE_MESSAGE_BOX, True, False)
    text = font.render(message, True, WHITE)
    
    width  = font.size(message)[0] + MESSAGE_BOX_MARGIN_WIDTH * 2 + MESSAGE_BOX_BORDER * 2
    height = font.size(message)[1] + MESSAGE_BOX_MARGIN_HEIGTH * 2 + MESSAGE_BOX_BORDER * 2
    
    if frame_left == 0:
        frame_left = VIEW_WIDTH / 2 - width / 2
    
    rect = pygame.Rect(frame_left, frame_top, width, height)
    pygame.draw.rect(screen, BLACK, rect)
    pygame.draw.rect(screen, BLUE, rect, MESSAGE_BOX_BORDER)
    
    text_top = frame_top + MESSAGE_BOX_BORDER + MESSAGE_BOX_MARGIN_HEIGTH 
    text_left = frame_left + MESSAGE_BOX_BORDER + MESSAGE_BOX_MARGIN_WIDTH 
    screen.blit(text, [text_left, text_top])
    

def main():
    
    """ Main function for the game. """
    pygame.init()
 
    # Set the width and height of the screen [width,height]
    screen = pygame.display.set_mode([VIEW_WIDTH, VIEW_HEIGHT])
 
    pygame.display.set_caption("GoatJump")
 
    game = Game()
    
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    processing = "Nothing"

    # -------- Main Program Loop -----------
    while not done:
          
        # Event Processing
        done = game.process_events()
                
        # Game Logic
        game.update()
            
        # Drawing        
        game.render(screen)
         
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
        # Limit to 60 frames per second
        clock.tick(FRAMES_PER_SECOND)
        
 
    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()
    
 
if __name__ == "__main__":
    main()
