import pygame
import math
import random
from constants import *
from sprites import *

class View():
    
    def __init__(self):
        self.x_offset = 0
        self.y_offset = 0
    

    def rect(self):
        return pygame.Rect(self.x_offset, self.y_offset, VIEW_WIDTH, VIEW_HEIGHT)
    
    
    def vertical_scroll_zone_lower(self):
        return pygame.Rect(self.x_offset, self.y_offset + VERTICAL_SCROLL_FLOOR, VIEW_WIDTH, VIEW_HEIGHT - VERTICAL_SCROLL_FLOOR)
    
    def vertical_scroll_zone_higher(self):
        return pygame.Rect(self.x_offset, self.y_offset, VIEW_WIDTH, VERTICAL_SCROLL_CEILING)    
    


class Level():
    
    def __init__(self):
        self.width = 3000
        self.height = 1000
        self.platforms = []
        self.platforms.append(Platform(50,  150, 180, 30))
        self.platforms.append(Platform(250, 300, 180, 30))
        self.platforms.append(Platform(450, 450, 180, 30))
        self.platforms.append(Platform(250, 600, 180, 30))
        self.platforms.append(Platform(450, 750, 180, 30))
        self.platforms.append(Platform(650, 680, 180, 30))
        self.platforms.append(Platform(850, 610, 180, 30))
        self.platforms.append(Platform(970, 540, 100, 30))
        self.platforms.append(Platform(1070, 470, 80, 20))
        
        self.view = View()
    
    
    def update(self, goat):
        if self.view.vertical_scroll_zone_lower().collidepoint(goat.x, goat.y):
            if goat.y < self.height - (VIEW_HEIGHT - VERTICAL_SCROLL_FLOOR):
                self.view.y_offset = goat.y - VERTICAL_SCROLL_FLOOR
            
        if self.view.vertical_scroll_zone_higher().collidepoint(goat.x, goat.y):
            if goat.y > VERTICAL_SCROLL_CEILING:
                self.view.y_offset = goat.y - VERTICAL_SCROLL_CEILING
                
        self.view.x_offset = goat.x - GOAT_X_OFFSET
        
    
    def render(self, screen):

        # platforms
        for platform in self.platforms:            
            if self.view.rect().colliderect(platform):
                platform.render(screen, self.view)
