import pygame
import constants

#-------------------------------------------------
#


class SpriteFrame():
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


#
#-------------------------------------------------


#-------------------------------------------------
#


class SpriteSheet():
    
    def __init__(self, image_filename, sprite_map):
        self.sprite_sheet = pygame.image.load(image_filename).convert()
        self.sprite_map = sprite_map
                
    def get_frame(self, name):
        image = None
        
        if name in self.sprite_map:
            frame = self.sprite_map[name]
            
            #Create a new blank image
            image = pygame.Surface([frame.width, frame.height]).convert()
            image.blit(self.sprite_sheet, (0, 0), (frame.x, frame.y, frame.width, frame.height))
            
            image.set_colorkey(constants.BLACK)
            
        return image


#
#-------------------------------------------------
