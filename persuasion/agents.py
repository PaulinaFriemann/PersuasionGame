import pygame
import movements
import behaviors
import math


class Sensor:

    def __init__(self, personal_space, center):
        self.radius = personal_space
        self.center = center

    def update(self, rect):
        self.center = rect.center

    def distance(self, rect):
        center_rect = rect.center
        return math.sqrt((center_rect[0] - self.center[0]) ** 2 + (center_rect[1] - self.center[1]) ** 2)

    def direction(self, rect):
        return [a - b for a,b in zip(self.center, rect.center)]

    

class Agent:
    def __init__(self, x, y, color, screen, movement=movements.idle, behavior=behaviors.do_nothing, player=None):
        self.color = color
        self.speed = [0, 0]
        self.screen = screen
        self.rect = pygame.Rect(x - 6 / 2, y - 6 / 2, 6, 6)
        self.speed_modificator = 1
        self.personalspace = 20
        self.sensor = Sensor(self.personalspace, self.rect.center)
        self.movement = movement
        self.behavior = behavior
        self.player = player
        
        self.path = [(0,0)]
        self.step=0

        if movement == movements.move_path:
            self.defaultpath = movements.path_circle(20)
            self.path = movements.path_circle(20)
            self.step = 0      

        if behavior == behaviors.avoid:
            self.runaway = False
    
    def move(self, speed):
        speed = map(lambda x: self.speed_modificator * x, speed)
        self.rect = self.rect.move(speed)
        self.sensor.update(self.rect)

    def update(self):
        self.behavior(self)
        self.movement(self)


class Player(Agent):
    def __init__(self, x, y, color, screen):

        Agent.__init__(self, x, y, color, screen)
        self.step = 0
        #self.speed_modificator = 3

    def move(self, speed):

        self.speed = map(lambda x: self.speed_modificator * x, self.speed)

        new_x = self.rect.bottomright[0] + self.speed[0]
        if self.screen.get_width() > new_x > (0 + self.rect.width):
            self.rect = self.rect.move(self.speed)
        else:
            self.rect = self.rect.move([0, self.speed[1]])

    def update(self):
        self.move(self.speed)

    def colorup(self, dh=0, ds=0, dv=0):
        h, s, v, a = self.color.hsva
        self.color.hsva = (min(h + dh, 255), min(s + ds, 100), min(v + dv, 100), a)
