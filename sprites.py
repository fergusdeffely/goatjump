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
        self.start_angle = 5
        self.swing = {}
        
        if motion_type == "fast":
            self.power_increment = 1.2
            self.start_angle = 15
            
        elif motion_type == "faster":
            self.power_increment = 1.4
            self.start_angle = 16
    
    
    def get_step(self):
        if self.motion_type == "basic":
            step = 2
        elif self.motion_type == "fast":
            step = 3
        elif self.motion_type == "faster":
            step = 4
        
        return step
    
    
    def get_swing(self, degrees, turn):

        step = self.get_step()
        
        if degrees > 0 and degrees < 90:
            return step
        elif degrees >= 90 and turn == UPSWING_TURN:
            return 0
        elif degrees >= 90 and turn == DOWNSWING_TURN:
            return step
        elif degrees <= 0:
            return 0
    
    
    def trace(self):
        print ("turn = 1: ")
        message = ""
        for n in range(91):
            if (n, 1) in self.swing:
                message += str(self.swing[(n, 1)])
                if n < 90: 
                    message += ", "
        print(message)
        
        print ("turn = -1: ")
        message = ""
        for n in range(91):
            if (n, -1) in self.swing:
                message += str(self.swing[(n, -1)])
                if n < 90:
                    message += ", "
        print(message)
        
        

class Goat():
    
    def __init__(self, jumpstate = "pregame"):
        self.x = GOAT_X_POSITION
        self.y = VERTICAL_SCROLL_CEILING
        self.speed_x = 0
        self.speed_y = 0
        self.turn = UPSWING_TURN

        # jumping
        # jumpstates: pregame, aiming, powering, midair, deaded
        self.jumpstate = jumpstate
        self.aiming_phase = "none"
        self.speed_accumulation_bonus = 0
        self.current_platform = None
        self.colour = GREEN
        
        self.radius = 20
    
    def to_view_coords(self, view):
        return {"x":self.x - view.x_offset, "y":self.y - view.y_offset}
        
        
    def adjusted_speed(self, speed):
        return speed
    

    def update(self, level):
        if self.jumpstate == "aiming":
            angular_motion = self.current_platform.indicator_motion.get_swing(self.angle, self.turn)
            
            if angular_motion == 0:
                if self.turn == UPSWING_TURN:
                    self.turn = DOWNSWING_TURN
                else:
                    self.jumpstate = "deaded"
            else:
                self.angle += angular_motion * self.turn
                if self.angle > 90:
                    self.angle = 90

        elif self.jumpstate == "powering":
            if self.radius < 82:
                self.radius += self.current_platform.indicator_motion.power_increment
            
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
                    self.turn = UPSWING_TURN
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
        coords = self.to_view_coords(view)
        pygame.draw.ellipse(screen, self.colour, [coords["x"] - 10, coords["y"] - 10, 20, 20], 0)
        
        
    def render_midair(self, screen, view):
        coords = self.to_view_coords(view)
        pygame.draw.ellipse(screen, self.colour, [coords["x"] - 10, coords["y"] - 10, 20, 20], 0)        


    def render_power(self, screen, view):
        coords = self.to_view_coords(view)
        
        colour = pygame.Color(0, 255, 0, 50)
        
        if self.radius >= DIRECTION_INDICATOR_LENGTH:
            colour = pygame.Color(255, 0, 0, 50)
        elif self.radius >= DIRECTION_INDICATOR_LENGTH - 10:
            colour = pygame.Color(255, 255, 0, 50)
        
        pygame.draw.ellipse(screen, colour, [coords["x"] - self.radius, coords["y"] - self.radius, self.radius * 2, self.radius * 2])
        rad = self.radius - 10
        pygame.draw.ellipse(screen, BLACK, [coords["x"] - rad, coords["y"] - rad, rad * 2, rad * 2])
        
        # Power limit
        rad = DIRECTION_INDICATOR_LENGTH - 2
        pygame.draw.ellipse(screen, WHITE, [coords["x"] - rad, coords["y"] - rad, rad * 2, rad * 2], 2)
        rad = DIRECTION_INDICATOR_LENGTH + 2
        pygame.draw.ellipse(screen, WHITE, [coords["x"] - rad, coords["y"] - rad, rad * 2, rad * 2], 2)        
        
        pygame.draw.ellipse(screen, self.colour, [coords["x"] - 10, coords["y"] - 10, 20, 20], 0)

    def render_direction(self, screen, view):
        coords = self.to_view_coords(view)
        
        arrow_head_x = coords["x"] + (DIRECTION_INDICATOR_LENGTH - 3) * math.cos(math.radians(self.angle))
        arrow_head_y = coords["y"] - (DIRECTION_INDICATOR_LENGTH - 3) * math.sin(math.radians(self.angle))
        arrow_shaft_x = coords["x"] + (DIRECTION_INDICATOR_LENGTH - 8) * math.cos(math.radians(self.angle))
        arrow_shaft_y = coords["y"] - (DIRECTION_INDICATOR_LENGTH - 8) * math.sin(math.radians(self.angle))       
        arrow_head_left_x = coords["x"] + (DIRECTION_INDICATOR_LENGTH - 15) * math.cos(math.radians(self.angle + 10))
        arrow_head_left_y = coords["y"] - (DIRECTION_INDICATOR_LENGTH - 15) * math.sin(math.radians(self.angle + 10))
        arrow_head_right_x = coords["x"] + (DIRECTION_INDICATOR_LENGTH - 15) * math.cos(math.radians(self.angle - 10))
        arrow_head_right_y = coords["y"] - (DIRECTION_INDICATOR_LENGTH - 15) * math.sin(math.radians(self.angle - 10)) 
        
        pygame.draw.line(screen, WHITE, [coords["x"], coords["y"]], [arrow_shaft_x, arrow_shaft_y], 6)
        pygame.draw.polygon(screen, WHITE, [[arrow_head_x, arrow_head_y], [arrow_head_left_x, arrow_head_left_y], [arrow_head_right_x, arrow_head_right_y]])
        #pygame.draw.line(screen, WHITE, [to_x, to_y], [arrow_head_right_x, arrow_head_right_y], 2)
        #pygame.draw.line(screen, WHITE, [to_x, to_y], [arrow_head_right_x, arrow_head_right_y], 2)        
        
        pygame.draw.ellipse(screen, self.colour, [coords["x"] - 10, coords["y"] - 10, 20, 20], 0)


    def render_deaded(self, screen, view):
        coords = self.to_view_coords(view)
        pygame.draw.ellipse(screen, WHITE, [coords["x"] - 10, coords["y"] - 10, 20, 20], 0)        
    
    
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
                
        font = pygame.font.SysFont('Calibri', 15, True, False)
        text = font.render(info, True, RED)
        screen.blit(text, [350, 10])

        
    def get_debug_info(self):
        return "({:.2f}, {:.2f}) @{}: jumpstate {}".format(self.x, self.y, self.radius, self.jumpstate)


    def get_speed_accumulation_bonus(self):
        return self.speed_accumulation_bonus
    
        
    def do_actionkey_down(self):
        if self.jumpstate == "aiming":
            if self.turn == UPSWING_TURN:
                self.speed_accumulation_bonus = 20
            else:
                self.speed_accumulation_bonus = 0
                
            self.jumpstate = "powering"
            
        elif self.jumpstate == "powering":
            if self.radius <= DIRECTION_INDICATOR_LENGTH:
                power = self.radius
            else:
                power = 20

            self.speed_x =  math.cos(math.radians(self.angle)) * power * G
            self.speed_y = -math.sin(math.radians(self.angle)) * power * G * 1.5                
            self.current_platform = None
            self.radius = 20
            
            self.jumpstate = "midair"
