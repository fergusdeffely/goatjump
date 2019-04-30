import pygame
import math
import random
from level import *
from constants import *


class SpriteFrame():
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        

class SpriteSheet():
    
    def __init__(self, image_filename, sprite_map):
        self.sprite_sheet = pygame.image.load(image_filename).convert()
        self.sprite_map = sprite_map
                
    def get_frame(self, name):
        image = None
        
        if name in self.sprite_map:
            frame_details = self.sprite_map[name]
            
            #Create a new blank image
            image = pygame.Surface([frame_details.width, frame_details.height]).convert()
            
            image.blit(self.sprite_sheet, (0, 0), (frame_details.x, frame_details.y, frame_details.width, frame_details.height))
            
            image.set_colorkey(BLACK)
            
        return image



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
        
        

class Goat(pygame.sprite.Sprite):
    
    def __init__(self, jumpstate = "pregame"):
        
        # init Sprite
        super().__init__()
        
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
        
        self.sprite_sheet = SpriteSheet("images/goat_sprite_sheet.png", {"STANDING": SpriteFrame(0, 0, 25, 25), 
                                                                         "UP_JUMP": SpriteFrame(25, 0, 25, 25),
                                                                         "DOWN_JUMP": SpriteFrame(50, 0, 25, 25)})
        
        self.image = self.sprite_sheet.get_frame("STANDING")
        self.rect = self.image.get_rect()
        self.rect.x = GOAT_X_POSITION
        self.rect.y = VERTICAL_SCROLL_CEILING
        
    
    def refresh_view_coords(self, view):
        self.rect.x = self.x - view.x_offset
        self.rect.y = self.y - view.y_offset
        
        
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
                    self.y = platform.rect.top - self.rect.height + 4
                    self.speed_x = 0
                    self.speed_y = 0
                    self.radius = 20
                    self.angle = platform.indicator_motion.start_angle
                    self.colour = platform.colour
                    self.turn = UPSWING_TURN
                    self.jumpstate = "aiming"
                    self.current_platform = platform
                    self.image = self.sprite_sheet.get_frame("STANDING")
                    #self.aiming_phase = "first_pass"
                    break
                
            self.x += self.speed_x
            self.y += self.speed_y            
        
        if self.y > level.height:
            self.jumpstate = "deaded"
        
        level.update(self)
        
        self.refresh_view_coords(level.view)
        
        
    def test_for_landing(self, platform):
        newpos_x = self.x + self.adjusted_speed(self.speed_x)
        newpos_y = self.y + self.adjusted_speed(self.speed_y)

        if self.y + self.rect.height < platform.rect.top and newpos_y + self.rect.height >= platform.rect.top:
            if newpos_x > platform.rect.left and newpos_x < platform.rect.left + platform.rect.width:
                print ( "(%d, %d) %d x %d: Landing on (%d, %d) %d x %d: at speed %d" % (self.x, self.y, self.rect.x, self.rect.y, platform.rect.left, platform.rect.top, platform.rect.width, platform.rect.height, self.adjusted_speed(self.speed_y) ) )
                return True

        return False
        

    def render_power(self, screen, view):
        colour = pygame.Color(0, 255, 0, 50)
        
        if self.radius >= DIRECTION_INDICATOR_LENGTH:
            colour = pygame.Color(255, 0, 0, 50)
        elif self.radius >= DIRECTION_INDICATOR_LENGTH - 10:
            colour = pygame.Color(255, 255, 0, 50)
        
        pygame.draw.ellipse(screen, colour, [self.rect.x - self.radius, self.rect.y - self.radius, self.radius * 2, self.radius * 2])
        rad = self.radius - 10
        pygame.draw.ellipse(screen, BLACK, [self.rect.x - rad, self.rect.y - rad, rad * 2, rad * 2])
        
        # Power limit
        rad = DIRECTION_INDICATOR_LENGTH - 2
        pygame.draw.ellipse(screen, WHITE, [self.rect.x - rad, self.rect.y - rad, rad * 2, rad * 2], 2)
        rad = DIRECTION_INDICATOR_LENGTH + 2
        pygame.draw.ellipse(screen, WHITE, [self.rect.x - rad, self.rect.y - rad, rad * 2, rad * 2], 2)
        
        pygame.draw.ellipse(screen, self.colour, [self.rect.x - 10, self.rect.y - 10, 20, 20], 0)
        

    def render_direction(self, screen, view):        
        arrow_head_x = self.rect.x + (DIRECTION_INDICATOR_LENGTH - 3) * math.cos(math.radians(self.angle))
        arrow_head_y = self.rect.y - (DIRECTION_INDICATOR_LENGTH - 3) * math.sin(math.radians(self.angle))
        arrow_shaft_x = self.rect.x + (DIRECTION_INDICATOR_LENGTH - 8) * math.cos(math.radians(self.angle))
        arrow_shaft_y = self.rect.y - (DIRECTION_INDICATOR_LENGTH - 8) * math.sin(math.radians(self.angle))
        arrow_head_left_x = self.rect.x + (DIRECTION_INDICATOR_LENGTH - 15) * math.cos(math.radians(self.angle + 10))
        arrow_head_left_y = self.rect.y - (DIRECTION_INDICATOR_LENGTH - 15) * math.sin(math.radians(self.angle + 10))
        arrow_head_right_x = self.rect.x + (DIRECTION_INDICATOR_LENGTH - 15) * math.cos(math.radians(self.angle - 10))
        arrow_head_right_y = self.rect.y - (DIRECTION_INDICATOR_LENGTH - 15) * math.sin(math.radians(self.angle - 10)) 
        
        pygame.draw.line(screen, WHITE, [self.rect.x, self.rect.y], [arrow_shaft_x, arrow_shaft_y], 6)
        pygame.draw.polygon(screen, WHITE, [[arrow_head_x, arrow_head_y], [arrow_head_left_x, arrow_head_left_y], [arrow_head_right_x, arrow_head_right_y]])
        
        pygame.draw.ellipse(screen, self.colour, [self.rect.x - 10, self.rect.y - 10, 20, 20], 0)

    
    def render(self, screen, view):
        info = self.jumpstate + ": " + self.get_debug_info()
                
        if self.jumpstate == "aiming":
            # TODO: change frame 
            self.render_direction(screen, view)

        elif self.jumpstate == "powering":
            self.render_power(screen, view)
            self.render_direction(screen, view)
            
        #elif self.jumpstate == "midair":
            # TODO: change frame
            
        #elif self.jumpstate == "deaded":
            # TODO: change frame 
                
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
            
            self.image = self.sprite_sheet.get_frame("UP_JUMP")
            self.jumpstate = "midair"
