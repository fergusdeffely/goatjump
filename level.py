import pygame
import math
import random
from constants import *
from sprites import *

#-------------------------------------------------
#
#


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
    
    
    def get_coords(self, x, y):
        return (x - self.x_offset, y - self.y_offset)


#
#
#-------------------------------------------------


#-------------------------------------------------
#
#


class Level():
    
    def __init__(self, goat):
        self.width = 3000
        self.height = 1000
        self.goat = goat
        self.platforms = []
        self.snowflake_group = pygame.sprite.Group()
        
        #practice level
        self.platforms.append(Platform(20, 250, 500, 30))
        self.platforms.append(Platform(200, 150, 100, 30))
        self.platforms.append(Platform(450, 400, 500, 30))        
        self.platforms.append(Platform(800, 300, 100, 30))
        self.platforms.append(Platform(900, 550, 500, 30))
        self.platforms.append(Platform(1200, 450, 100, 30))
        self.platforms.append(Platform(1350, 700, 500, 30))
        self.platforms.append(Platform(1800, 600, 100, 30))
        
        self.snowflake_group.add(Snowflake(0, 5, 200, 80))
        self.snowflake_group.add(Snowflake(2, 5, 260, 70))
        self.snowflake_group.add(Snowflake(5, 5, 320, 60))
        self.snowflake_group.add(Snowflake(7, 5, 380, 70))
        self.snowflake_group.add(Snowflake(1, 5, 440, 80))
        self.snowflake_group.add(Snowflake(3, 5, 500, 90))
        self.snowflake_group.add(Snowflake(4, 5, 560, 100))
        self.snowflake_group.add(Snowflake(6, 5, 620, 110))
        self.snowflake_group.add(Snowflake(0, 5, 680, 120))
        
        #level 1
        #self.platforms.append(Platform(20, 250, 150, 30))
        #self.platforms.append(Platform(850,290, 300, 30))
        #self.platforms.append(Platform(250,250, 300, 30))
        #self.platforms.append(Platform(550,270, 300, 30))
        
        #level 2
        #self.platforms.append(Platform(20, 250, 150, 30, "fast"))
        #self.platforms.append(Platform(250,250, 300, 30, "fast"))
        #self.platforms.append(Platform(550,270, 300, 30, "fast"))
        #self.platforms.append(Platform(850,290, 300, 30, "fast"))

        #level 3
        #self.platforms.append(Platform(20, 250, 150, 30, "faster"))
        #self.platforms.append(Platform(250,250, 300, 30, "faster"))
        #self.platforms.append(Platform(550,270, 300, 30, "faster"))
        #self.platforms.append(Platform(850,290, 300, 30, "faster"))
        
        #level 4
        #self.platforms.append(Platform(20, 250, 150, 30))
        #self.platforms.append(Platform(250,350, 150, 30, "fast"))
        #self.platforms.append(Platform(470,350, 150, 30, "faster"))
        #self.platforms.append(Platform(640,290, 200, 30))
                                       
        # Advanced level
        #self.platforms.append(Platform(50,  150, 180, 30, "faster"))
        #self.platforms.append(Platform(250, 300, 180, 30, "faster"))
        #self.platforms.append(Platform(450, 450, 180, 30, "fast"))
        #self.platforms.append(Platform(260, 600, 180, 30))
        #self.platforms.append(Platform(450, 750, 180, 30, "fast"))
        #self.platforms.append(Platform(650, 680, 180, 30))
        #self.platforms.append(Platform(850, 610, 180, 30))
        #self.platforms.append(Platform(970, 540, 100, 30, "faster"))
        #self.platforms.append(Platform(1070, 470, 80, 20))
        #self.platforms.append(Platform(1200, 570, 70, 20, "fast"))
        #self.platforms.append(Platform(1320, 450, 50, 20, "fast"))
        #self.platforms.append(Platform(1200, 570, 80, 20, "fast"))
        #self.platforms.append(Platform(1400, 540, 70, 20, "fast"))
        #self.platforms.append(Platform(1600, 510, 60, 20, "fast"))
        #self.platforms.append(Platform(1800, 480, 60, 20, "fast"))
        #self.platforms.append(Platform(2000, 450, 50, 20, "fast"))
        
        self.view = View()        
        
        
    def scroll(self, x, y):
        
        if self.view.vertical_scroll_zone_lower().collidepoint(x, y):
            if y < self.height - (VIEW_HEIGHT - VERTICAL_SCROLL_FLOOR):
                self.view.y_offset = y - VERTICAL_SCROLL_FLOOR
        elif self.view.vertical_scroll_zone_higher().collidepoint(x, y):
            if y > VERTICAL_SCROLL_CEILING:
                self.view.y_offset = y - VERTICAL_SCROLL_CEILING
                
        self.view.x_offset = x - GOAT_X_POSITION
        
    
    def update(self):
        for snowflake in self.snowflake_group:
            snowflake.refresh_view_coords(self.view)
        self.snowflake_group.update()
        
    
    def draw(self, screen):

        # platforms
        for platform in self.platforms:            
            if self.view.rect().colliderect(platform):
                platform.render(screen, self.view)
                
        
        self.snowflake_group.draw(screen)


#
#
#-------------------------------------------------
