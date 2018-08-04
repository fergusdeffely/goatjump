import pygame
import math
import random
from level import *
from constants import *



class Platform():
    
    def __init__(self, left, top, width, height, motion_type = "basic"):
        self.rect = pygame.Rect(left, top, width, height)
        self.indicator_motion = IndicatorMotion(motion_type)
        self.colour = GREEN
        if motion_type == "fast":
            self.colour = PINK
        elif motion_type == "faster":
            self.colour = RED
    
    
    def to_view_coords(self, view):
        return pygame.Rect(self.rect.left - view.x_offset, self.rect.top - view.y_offset, self.rect.width, self.rect.height)
    

    def render(self, screen, view):
        pygame.draw.rect(screen, self.colour, self.to_view_coords(view) )
        
        
        
class IndicatorMotion():
    
    def __init__(self, motion_type):
        self.motion_type = motion_type
        self.power_increment = 1
        self.start_angle = 0
        self.swing = {}
        
        if motion_type == "basic":
            self.start_angle = 16
            for n in range(0, 91, 2):
                self.swing[(n, 1)] = self.swing[(n, -1)] = 2
                
            self.swing[(0, -1)] = 0
            self.swing[(90, 1)] = 0
            
        elif motion_type == "fast":
            self.power_increment = 1.5
            self.start_angle = 15
            for n in range(0, 91, 3):
                self.swing[(n, 1)] = self.swing[(n, -1)] = 3
                
            self.swing[(0, -1)] = 0
            self.swing[(90, 1)] = 0
            
        elif motion_type == "faster":
            self.power_increment = 2
            self.start_angle = 16
            for n in range(0, 91, 4):
                self.swing[(n, 1)] = self.swing[(n, -1)] = 4
                
            self.swing[(0, -1)]  = 0
            self.swing[(88, 1)]  = 2
            self.swing[(90, -1)] = 2
            self.swing[(90, 1)]  = 0
    
    
    def get_swing(self, degrees, turn):
        return self.swing[(degrees, turn)]
    
    
    def trace(self):
        print ("turn = 1: ")
        message = ""
        for n in range(91):
            if self.swing.__contains__((n, 1)):
                message += str(self.swing[(n, 1)])
                if n < 90: 
                    message += ", "
        print(message)
        
        print ("turn = -1: ")
        message = ""
        for n in range(91):
            if self.swing.__contains__((n, -1)):
                message += str(self.swing[(n, -1)])
                if n < 90:
                    message += ", "
        print(message)
        
        

class Goat():
    
    def __init__(self):
        self.x = GOAT_X_POSITION
        self.y = VERTICAL_SCROLL_CEILING
        self.speed_x = 0
        self.speed_y = 0
        self.turn = 1

        # jumping
        # jumpstates: aiming, powering, midair, deaded
        self.jumpstate = "midair"
        self.aiming_phase = "none"
        self.speed_accumulation_bonus = 0
        self.current_platform = None
        self.colour = GREEN
        
        self.radius = 20
        
        
    def to_view_coords(self, view):
        return {"x":self.x - view.x_offset, "y":self.y - view.y_offset}
        
        
    def adjusted_speed(self, speed):
        return speed


    def turn(self, angle):
        return angle * self.turn
    

    def update(self, level):
        if self.jumpstate == "aiming":
            angular_motion = self.current_platform.indicator_motion.get_swing(self.angle, self.turn)
            
            if angular_motion == 0:
                if self.turn == 1:
                    self.turn = -1
                else:
                    self.jumpstate = "deaded"
            else:
                self.angle += angular_motion * self.turn

        elif self.jumpstate == "powering":
            if self.radius < 30:
                self.radius += 1 * self.current_platform.indicator_motion.power_increment
            elif self.radius < 40:
                self.radius += 2 * self.current_platform.indicator_motion.power_increment
            elif self.radius < 82:
                self.radius += 3 * self.current_platform.indicator_motion.power_increment
                
        elif self.jumpstate == "midair":            
            self.speed_y += G

            for platform in level.platforms:
                if self.test_for_landing(platform):
                    self.y = platform.rect.top - self.radius / 2 + 2
                    self.speed_x = 0
                    self.speed_y = 0
                    self.radius = 20
                    self.angle = platform.indicator_motion.start_angle
                    self.colour = platform.colour
                    self.turn = 1
                    self.jumpstate = "aiming"
                    self.current_platform = platform
                    #self.aiming_phase = "first_pass"
                    break
                
            self.x += self.speed_x
            self.y += self.speed_y            
        
        if self.y > level.height:
            self.jumpstate = "deaded"
        
        level.update(self)
        
        
    def test_for_landing(self, platform):
        newpos_x = self.x + self.adjusted_speed(self.speed_x)
        newpos_y = self.y + self.adjusted_speed(self.speed_y)

        if self.y < platform.rect.top and newpos_y >= platform.rect.top:
            if newpos_x > platform.rect.left and newpos_x < platform.rect.left + platform.rect.width:
                print ( "(%d, %d): Landing on (%d, %d) %d x %d: at speed %d" % (self.x, self.y, platform.rect.left, platform.rect.top, platform.rect.width, platform.rect.height, self.adjusted_speed(self.speed_y) ) )
                return True

        return False


    def render_grounded(self, screen, view):
        view_coords = self.to_view_coords(view)
        pygame.draw.ellipse(screen, self.colour, [view_coords["x"] - 10, view_coords["y"] - 10, 20, 20], 0)
        
        
    def render_midair(self, screen, view):
        view_coords = self.to_view_coords(view)
        pygame.draw.ellipse(screen, self.colour, [view_coords["x"] - 10, view_coords["y"] - 10, 20, 20], 0)        


    def render_power(self, screen, view):
        view_coords = self.to_view_coords(view)
        
        pen = 5
        if self.radius > 30:
            pen = 4
        elif self.radius > 40:
            pen = 3
        elif self.radius > 50:
            pen = 2
        elif self.radius > 65:
            pen = 1
        
        colour = BLUE
        target_colour = YELLOW
        if self.radius > DIRECTION_INDICATOR_LENGTH:
            colour = RED
            target_colour = WHITE

        pygame.draw.ellipse(screen, target_colour, [view_coords["x"] - DIRECTION_INDICATOR_LENGTH, view_coords["y"] - DIRECTION_INDICATOR_LENGTH, DIRECTION_INDICATOR_LENGTH * 2, DIRECTION_INDICATOR_LENGTH * 2], 3)
        pygame.draw.ellipse(screen, colour, [view_coords["x"] - self.radius, view_coords["y"] - self.radius, self.radius * 2, self.radius * 2], pen)
        

    def render_direction(self, screen, view):
        view_coords = self.to_view_coords(view)
        
        to_x = view_coords["x"] + DIRECTION_INDICATOR_LENGTH * math.cos(math.radians(self.angle))
        to_y = view_coords["y"] - DIRECTION_INDICATOR_LENGTH * math.sin(math.radians(self.angle))
        
        pygame.draw.line(screen, WHITE, [view_coords["x"], view_coords["y"]], [to_x, to_y], 2)


    def render_deaded(self, screen, view):
        view_coords = self.to_view_coords(view)
        pygame.draw.ellipse(screen, WHITE, [view_coords["x"] - 10, view_coords["y"] - 10, 20, 20], 0)        
    
    
    def render(self, screen, view):
        info = self.jumpstate + ": " + self.get_debug_info()

        if self.jumpstate == "aiming":
            self.render_grounded(screen, view)
            self.render_direction(screen, view)

        elif self.jumpstate == "powering":
            self.render_power(screen, view)
            self.render_direction(screen, view)
            
        elif self.jumpstate == "midair":
            self.colour = CYAN
            self.render_midair(screen, view)            
            
        elif self.jumpstate == "deaded":
            self.render_deaded(screen, view)
                
        font = pygame.font.SysFont('Calibri', 25, True, False)
        text = font.render(info, True, RED)
        screen.blit(text, [200, 50])

        
    def get_debug_info(self):
        return "({:.2f}, {:.2f}) @{}: jumpstate {}".format(self.x, self.y, self.radius, self.jumpstate)


    def get_speed_accumulation_bonus(self):
        return self.speed_accumulation_bonus
    
        
    def do_actionkey_down(self):
        if self.jumpstate == "aiming":
            if self.turn == 1:
                self.speed_accumulation_bonus = 20
            else:
                self.speed_accumulation_bonus = 0
                
            self.jumpstate = "powering"
            
        elif self.jumpstate == "powering":
            if self.radius <= 50:
                power = self.radius
            else:
                power = 20

            self.speed_x =  math.cos(math.radians(self.angle)) * power * G
            self.speed_y = -math.sin(math.radians(self.angle)) * power * G * 1.5                
            self.current_platform = None
            self.radius = 20
            
            self.jumpstate = "midair"
