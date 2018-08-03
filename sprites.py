import pygame
import math
import random
from level import *
from constants import *



class Platform():
    
    def __init__(self, left, top, width, height):
        self.rect = pygame.Rect(left, top, width, height)

    
    def to_view_coords(self, view):
        return pygame.Rect(self.rect.left - view.x_offset, self.rect.top - view.y_offset, self.rect.width, self.rect.height)
    

    def render(self, screen, view):
        pygame.draw.rect(screen, GREEN, self.to_view_coords(view) )
        


class Goat():
    
    def __init__(self):
        self.x = GOAT_X_OFFSET
        self.y = VERTICAL_SCROLL_CEILING
        self.speed_x = 0
        self.speed_y = 0

        # jumping
        # jumpstates: grounded, powering, aiming, midair, cleanup
        self.jumpstate = "midair"
        self.current_platform = None
        
        self.radius = 20
        
        
    def to_view_coords(self, view):
        return {"x":self.x - view.x_offset, "y":self.y - view.y_offset}
        
        
    def adjusted_speed(self, speed):
        return speed


    def update(self, level):
        movement_offset = {"x":0, "y":0}
        
        if self.jumpstate == "powering":
            if self.radius > 5:
                self.radius -= 1
                
        elif self.jumpstate == "aiming_first_pass":
            if self.angle + PI / 100 >= PI /2:
                self.angle = PI / 2
                self.jumpstate = "aiming_second_pass"
            else:
                self.angle += PI / 100
                
        elif self.jumpstate == "aiming_second_pass":
            if self.angle - PI / 100 <= 0:
                self.angle = 0
                self.jumpstate = "deaded"
            else:
                self.angle -= PI / 100
                
        #elif self.jumpstate == "grounded":
            # do checks for obstacles, falling, etc
            #movement_offset["x"] = self.adjusted_speed(self.speed_x)
                
        elif self.jumpstate == "midair":            
            self.speed_y += G

            for platform in level.platforms:
                if self.landing(platform):
                    self.y = platform.rect.top - self.radius / 2 + 2
                    self.current_platform = platform
                    self.speed_x = 0
                    self.speed_y = 0
                    self.jumpstate = "grounded"
                    break
                
            self.x += self.speed_x
            self.y += self.speed_y            
            
            #movement_offset["x"] = self.adjusted_speed(self.speed_x)
            #movement_offset["y"] = self.adjusted_speed(self.speed_y)
            

        
        if self.y > level.height:
            self.jumpstate = "deaded"
        
        level.update(self)
        
        
    def landing(self, platform):
        newpos_x = self.x + self.adjusted_speed(self.speed_x)
        newpos_y = self.y + self.adjusted_speed(self.speed_y)

        if self.y < platform.rect.top and newpos_y >= platform.rect.top:
            if newpos_x > platform.rect.left and newpos_x < platform.rect.left + platform.rect.width:
                print ( "(%d, %d): Landing on (%d, %d) %d x %d: at speed %d" % (self.x, self.y, platform.rect.left, platform.rect.top, platform.rect.width, platform.rect.height, self.adjusted_speed(self.speed_y) ) )
                return True

        return False


    def render_grounded(self, screen, view):
        view_coords = self.to_view_coords(view)
        pygame.draw.ellipse(screen, GREEN, [view_coords["x"] - 10, view_coords["y"] - 10, 20, 20], 0)
        
        
    def render_midair(self, screen, view):
        view_coords = self.to_view_coords(view)
        pygame.draw.ellipse(screen, YELLOW, [view_coords["x"] - 10, view_coords["y"] - 10, 20, 20], 0)        


    def render_power(self, screen, view):
        view_coords = self.to_view_coords(view)
        colour = BLUE
        if self.radius < 20:
            colour = RED
            
        pygame.draw.ellipse(screen, colour, [view_coords["x"] - self.radius, view_coords["y"] - self.radius, self.radius * 2, self.radius * 2], 0)
        

    def render_direction(self, screen, view):
        view_coords = self.to_view_coords(view)
        
        to_x = view_coords["x"] + self.radius * 2 * math.cos(self.angle)
        to_y = view_coords["y"] - self.radius * 2 * math.sin(self.angle)
        
        pygame.draw.line(screen, BLACK, [view_coords["x"], view_coords["y"]], [to_x, to_y], 2)


    def render_deaded(self, screen, view):
        view_coords = self.to_view_coords(view)
        pygame.draw.ellipse(screen, BLACK, [view_coords["x"] - 10, view_coords["y"] - 10, 20, 20], 0)        
    
    
    def render(self, screen, view):
        info = self.jumpstate + ": " + self.get_debug_info()
        
        if self.jumpstate == "grounded": 
            self.render_grounded(screen, view)
            
        elif self.jumpstate == "midair":
            self.render_midair(screen, view)
            
        elif self.jumpstate == "powering":
            self.render_power(screen, view)
        
        elif self.jumpstate == "aiming_first_pass" or self.jumpstate == "aiming_second_pass":
            self.render_power(screen, view)
            self.render_direction(screen, view)
            
        elif self.jumpstate == "deaded":
            self.render_deaded(screen, view)
                
        font = pygame.font.SysFont('Calibri', 25, True, False)
        text = font.render(info, True, RED)
        screen.blit(text, [200, 50])
        
    def get_debug_info(self):
        return "({:.2f}, {:.2f}) @{}: jumpstate {}".format(self.x, self.y, self.radius, self.jumpstate)
        
    def do_actionkey_down(self):
        if self.jumpstate == "grounded":
            #self.x = random.randrange(100, 150)
            #self.y = random.randrange(250, 400)
            self.radius = 50
            self.jumpstate = "powering"            
            
        elif self.jumpstate == "powering":
            self.angle = PI / 12
            self.jumpstate = "aiming_first_pass"
            
        elif self.jumpstate == "aiming_first_pass" or self.jumpstate == "aiming_second_pass":            
            self.speed_x =  math.cos(self.angle) * self.radius * G
            self.speed_y = -math.sin(self.angle) * self.radius * G * 1.5
            if self.jumpstate == "aiming_fist_pass":
                # speed accumulation bonus
                self.speed_x += 20
                
            self.current_platform = None
            self.radius = 20
            self.jumpstate = "midair"
