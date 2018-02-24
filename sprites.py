import pygame
import math
import random
from constants import *


class Indicator():
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.radius = 50
        self.angle = 0
        self.t = 0
        # indicator states: clear, power, direction, cleanup
        self.state = "clear"

        
    def update(self):
        if self.state == "power":
            if self.radius > 5:
                self.radius -= 1
                
        elif self.state == "direction":
            if self.angle < PI:
                self.angle -= PI / 180
                
        elif self.state == "launch":
            if self.t <= 30:
                self.t += 0.2


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
        dy = math.sin(self.angle) * self.radius * self.t + G / 10 * self.t * self.t
        pygame.draw.rect(screen, BLACK, [self.x + dx, self.y + dy, 2, 2], 1)
        
        
    def render(self, screen):
        
        info = self.state
        
        if self.state == "power":
            self.render_power(screen)
            info += ": " + str(self.radius)
            
        elif self.state == "direction":
            self.render_power(screen)
            self.render_direction(screen)
            info += ": " + str(self.radius)
            
        elif self.state == "launch":
            self.render_power(screen)
            self.render_direction(screen)
            self.render_trajectory(screen)
            info += ": " + str(self.radius)
                
        font = pygame.font.SysFont('Calibri', 25, True, False)
        text = font.render(info, True, RED)
        screen.blit(text, [400, 450])
        
        
    def do_actionkey_down(self):

        if self.state == "clear":
            self.x = random.randrange(100, 150)
            self.y = random.randrange(250, 400)
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
