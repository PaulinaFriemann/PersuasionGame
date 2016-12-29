import pygame
import movements
from enum import Enum
import __builtin__


class Attitude(Enum):
    neutral = 0
    avoiding = 1
    friendly = 2
    friends = 3

attitudes = [movements.idle, movements.avoid, movements.make_happy, movements.default]


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
        self.path = []
        self.step = 0
        self.defaultpath = []

        if self.attitude == Attitude.friendly:
            self.personalspace = 6
        
        self.set_path(movements.idle(self), default=True)
        self.defaultpath = self.path

        if movement == movements.circle:
            self.set_path(movements.circle(20), default=True)

        elif movement == movements.random_to_goal:
            self.goal = [self.rect.centerx + 20, self.rect.centery + 100]
            self.set_path(self.movement(self))
            self.set_default_path(movements.idle(self))

    def direction_to(self, rect):
        return [a - b for a,b in zip(self.rect.center, rect.center)]
    
    def move(self, speed):
        speed = map(lambda x: self.speed_modificator * x, speed)
        self.rect = self.rect.move(speed)

    def update(self):
        movements.move_path(self)

    def set_path(self, movement, default=False, step=0):
        self.step = step
        self.path = movement
        if default:
            self.defaultpath = self.path

    def set_default_path(self, movement):
        self.defaultpath = movement

    def on_enter_personal_space(self):
        try:
            self.set_path(attitudes[self.attitude.value](self))

        except AttributeError:
            self.set_path(attitudes[self.attitude](self))

        if self.attitude == Attitude.friendly:
            __builtin__.game.action_queue.add(self.change_attitude, [Attitude.friends], len(self.path))

    def on_collision(self, other):
        pass

    def change_attitude(self, attitude):
        if attitude != self.attitude:
            self.attitude = attitude


class Player(Agent):
    def __init__(self, x, y, color, screen):

        Agent.__init__(self, x, y, color, screen)

        #self.speed_modificator = 3

    def move(self, speed):
        self.speed = map(lambda x: self.speed_modificator * x, speed)

        new_x = self.rect.bottomright[0] + self.speed[0]
        if self.screen.get_width() > new_x > (0 + self.rect.width):
            self.rect = self.rect.move(speed)
        else:
            self.rect = self.rect.move([0, speed[1]])

    def update(self):
        if self.path == [[0,0]]:
            self.move(self.speed)
        else:
            movements.move_path(self)

    def colorup(self, dh=0, ds=0, dv=0):
        h, s, v, a = self.color.hsva
        self.color.hsva = (min(h + dh, 255), min(s + ds, 100), min(v + dv, 100), a)

    def on_enter_personal_space(self):
        pass

    def on_collision(self, other):
        if self.path == [[0,0]]:

            if other.attitude == Attitude.friendly:
                self.colorup(ds=1)
                self.set_path(movements.make_happy(self))
            else:
                self.set_path(movements.bounce_back(self))




    def happy_spin(self):
        self.spinning = True
        self.blocked = True
        self.block_counter = 12
        self.path = [[0, 0]]
        self.path = [[1, 1]] * 3
        self.path.extend([[-1, 1]] * 3)
        self.path.extend([[-1, -1]] * 3)
        self.path.extend([[1, -1]] * 3)
