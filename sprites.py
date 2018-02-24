import pygame
import math
import random
from constants import *


class Indicator():
    
    def __init__(self):
        self.x = 60
        self.y = 80
        self.speed_x = 0
        self.speed_y = 0
        self.radius = 20
        self.angle = 0
        self.t = 0
        # indicator states: clear, power, direction, cleanup
        self.state = "clear"
        self.current_surface = None

    def update(self, surfaces):
        if self.state == "power":
            if self.radius > 5:
                self.radius -= 1
                
        elif self.state == "direction":
            if self.angle < PI:
                self.angle -= PI / 180
                
        elif self.state == "launch":
            if self.t <= 30:
                self.t += 0.2

        # falling?
        if self.current_surface == None:
            for surface in surfaces:
                if self.landed_on(surface):
                    self.current_surface = surface
                    self.y = surface[1] - 10
                    self.speed_y = 0
                    break
                
        if self.current_surface == None:
            # must be falling
            self.speed_y += G
            
        self.x += self.speed_x
        self.y += self.speed_y
            
    def landed_on(self, surface):
        if self.y + self.speed_y > surface[1] and (self.x > surface[0] and self.x < surface [0] + surface [2]):
            return True

        return False

    def render_default(self, screen):
        
        pygame.draw.ellipse(screen, GREEN, [self.x - 10, self.y - 10, 20, 20], 0)


    def render_power(self, screen):

        colour = BLUE
        if self.radius < 20:
            colour = RED
            
        pygame.draw.ellipse(screen, colour, [self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2], 0)
        

    def render_direction(self, screen):
        
        to_x = self.x + self.radius * 2 * math.cos(self.angle)
        to_y = self.y + self.radius * 2 * math.sin(self.angle)
        
        pygame.draw.line(screen, BLACK, [self.x, self.y], [to_x, to_y], 2)
        
        
    def render_trajectory(self, screen):

        dx = math.cos(self.angle) * self.radius * self.t
        dy = math.sin(self.angle) * self.radius * self.t + G * self.t * self.t
        pygame.draw.rect(screen, BLACK, [self.x + dx, self.y + dy, 2, 2], 1)
        
    def render(self, screen):
        
        info = self.state + ": " + self.get_debug_info()
        
        if self.state == "clear":
            self.render_default(screen)
            
        elif self.state == "power":
            self.render_power(screen)
        
        elif self.state == "direction":
            self.render_power(screen)
            self.render_direction(screen)
            
        elif self.state == "launch":
            self.render_power(screen)
            self.render_direction(screen)
            self.render_trajectory(screen)
                
        font = pygame.font.SysFont('Calibri', 25, True, False)
        text = font.render(info, True, RED)
        screen.blit(text, [200, 50])
        
    def get_debug_info(self):
        surface = "Yes"
        if self.current_surface == None:
            surface = "No"
            
        return "({:.2f}, {:.2f}) @{}: surface {}".format(self.x, self.y, self.radius, surface)
        
    def do_actionkey_down(self):

        if self.state == "clear":
            #self.x = random.randrange(100, 150)
            #self.y = random.randrange(250, 400)
            self.radius = 50
            self.angle = 0
            self.t = 0
            self.state = "power"            
            
        elif self.state == "power":
            self.state = "direction"
            
        elif self.state == "direction":
            self.state = "launch"
            
        elif self.state == "launch":
            self.state = "clear"
