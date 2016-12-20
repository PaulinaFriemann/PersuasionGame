import pygame
import movements
import math
from enum import Enum


class Attitude(Enum):
    neutral = 0
    avoiding = 1
    friendly = 2

attitudes = [movements.do_nothing, movements.avoid, movements.make_happy]


class Agent:
    def __init__(self, x, y, color, screen, movement=movements.idle, attitude=Attitude.neutral, player=None):
        self.color = color
        self.speed = [0, 0]
        self.screen = screen
        self.rect = pygame.Rect(x - 6 / 2, y - 6 / 2, 6, 6)
        self.speed_modificator = 1
        self.personalspace = 20
        self.movement = movement
        self.attitude = attitude
        self.player = player
        self.distance_to_player = 999
        
        self.path = [(0,0)]
        self.step=0

        if movement == movements.move_path:
            self.defaultpath = movements.path_circle(20)
            self.path = movements.path_circle(20)
            self.step = 0      

        if attitude == Attitude.avoiding:
            self.runaway = False

    def direction_to(self, rect):
        return [a - b for a,b in zip(self.rect.center, rect.center)]
    
    def move(self, speed):
        speed = map(lambda x: self.speed_modificator * x, speed)
        self.rect = self.rect.move(speed)

    def update(self):
        #self.behavior(self)
        self.movement(self)

    def on_enter_personal_space(self):
        attitudes[self.attitude.value](self)


class Player(Agent):
    def __init__(self, x, y, color, screen):

        Agent.__init__(self, x, y, color, screen)
        self.blocked = False
        self.block_counter = 0
        self.bounce_speed = [0,0]
        #self.speed_modificator = 3

    def move(self, speed):

        speed = map(lambda x: self.speed_modificator * x, speed)

        new_x = self.rect.bottomright[0] + speed[0]
        if self.screen.get_width() > new_x > (0 + self.rect.width):
            self.rect = self.rect.move(speed)
        else:
            self.rect = self.rect.move([0, speed[1]])

    def update(self):
        if not self.blocked:
            self.move(self.speed)
        else:
            self.block_counter -= 1
            self.move(self.bounce_speed)
            if self.block_counter == 0:
                self.blocked = False

    def colorup(self, dh=0, ds=0, dv=0):
        h, s, v, a = self.color.hsva
        self.color.hsva = (min(h + dh, 255), min(s + ds, 100), min(v + dv, 100), a)

    def on_collision(self, other):
        if not self.blocked and other.attitude == Attitude.friendly:
            self.bounce_back()
            self.colorup(ds=1)

    def bounce_back(self):
        self.blocked = True
        self.block_counter = 15
        self.bounce_speed = map(lambda x: -x, self.speed)
