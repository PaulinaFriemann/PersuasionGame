import pygame
import movements
import behaviors


class Agent:
    def __init__(self, x, y, color, screen, movement=movements.idle, behavior=behaviors.do_nothing, player=None):
        self.color = color
        self.speed = [0, 0]
        self.screen = screen
        self.rect = pygame.Rect(x - 6 / 2, y - 6 / 2, 6, 6)
        self.speed_modificator = 1
        self.personalspace = 1000
        self.sensor = pygame.Rect(self.rect.centerx, self.rect.centery,
                                  self.rect.width * self.personalspace, self.rect.height * self.personalspace)
        self.movement = movement
        self.behavior = behavior

        if movement == movements.circle:
            self.path = movements.path_circle(20)
            self.step = 0

        if behavior == behaviors.avoid:
            self.runaway = False
            self.player = player

    def move(self, speed):
        speed = map(lambda x: self.speed_modificator * x, speed)
        self.rect = self.rect.move(speed)
        self.sensor = self.sensor.move(speed)

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
        if h + dh <= 255 and s + ds <= 100 and v + dv <= 100:
            self.color.hsva = (h + dh, s + ds, v + dv, a)
