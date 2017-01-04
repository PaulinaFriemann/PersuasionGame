import pygame
from enum import Enum
import settings
import movements
import gui


class Attitude(Enum):
    neutral = 0
    avoiding = 1
    friendly = 2
    friends = 3


collision_reactions = [movements.bounce_back, movements.bounce_back, movements.make_happy, movements.bounce_back]
personal_space_reactions = [movements.default, movements.avoid, movements.do_nothing, movements.make_happy]


class Agent:
    def __init__(self, x, y, color, movement=movements.idle, attitude=Attitude.neutral, cluster_member=False):
        self.color = color
        self.speed = [0, 0]
        self.width = 10
        self.rect = pygame.Rect(x - self.width / 2, y - self.width / 2, self.width, self.width)
        self.speed_modificator = 1
        self.personalspace = self.width*4
        self.default_movement = movement
        self.attitude = attitude
        self.distance_to_player = 999
        self.path = []
        self.step = 0
        self.cluster_member = cluster_member
        self.event = False
        self.goal = None

        self.set_path(self.default_movement, default=True)

        if movement == movements.random_to_goal:
            self.goal = [self.rect.centerx + 20, self.rect.centery + 100]
            self.set_path(self.default_movement)
            self.set_default_path(movements.idle)

    def direction_to(self, rect):
        return [a - b for a, b in zip(self.rect.center, rect.center)]

    def move(self, speed):
        speed = map(lambda x: self.speed_modificator * x, speed)
        self.rect = self.rect.move(speed)

    def update(self):
        movements.move_path(self)

    def set_path(self, movement, default=False, step=0):
        self.step = step
        self.path = movement(self)
        if default:
            self.default_movement = movement

    def set_default_path(self, movement):
        self.default_movement = movement

    def on_enter_personal_space(self):
        if not self.event:
            try:
                self.set_path(personal_space_reactions[self.attitude.value])

            except TypeError:
                self.set_path(personal_space_reactions[self.attitude])
            self.event = True

    def on_collision(self, other):
        try:
            self.set_path(collision_reactions[self.attitude.value])
        except TypeError:
            self.set_path(collision_reactions[self.attitude])

        self.event = True

        if self.attitude == Attitude.friendly:
            settings.game.action_queue.add(self.change_attitude, {"attitude": Attitude.friends}, len(self.path))
            try:
                settings.game.action_queue.add(self.set_path, {"movement": movements.follow, "default": True},
                                      len(self.path))
            except TypeError:
                settings.game.action_queue.add(self.set_path,
                                      {"movement": movements.follow, "default": True},
                                      len(self.path))

    def change_attitude(self, attitude):
        if attitude != self.attitude:
            self.attitude = attitude


class Dummy(Agent):

    def __init__(self, color, movement=movements.idle, attitude=Attitude.neutral,
                 cluster_member=False):
        Agent.__init__(self, 0, 0, color, movement, attitude)
        self.cluster_member = True


class Player(Agent):
    def __init__(self, x, y, color):

        Agent.__init__(self, x, y, color)
        self.name_area = pygame.Rect(self.rect.left, self.rect.top + 7, 30, 15)

        # self.speed_modificator = 3

    def move(self, speed):
        self.speed = map(lambda x: self.speed_modificator * x, speed)

        new_x = self.rect.bottomright[0] + self.speed[0]
        if settings.screen_width > new_x > (0 + self.rect.width):
            self.rect = self.rect.move(speed)

            self.name_area = self.name_area.move(speed)
        else:
            self.rect = self.rect.move([0, speed[1]])
            self.name_area.move_ip([0, speed[1]])

    def update(self):
        if self.path == [[0, 0]]:
            self.move(self.speed)
        else:
            movements.move_path(self)

    def colorup(self, dh=0, ds=0, dv=0):
        h, s, v, a = self.color.hsva
        self.color.hsva = (min(h + dh, 255), min(s + ds, 100), min(v + dv, 100), a)

    def on_enter_personal_space(self):
        pass

    def on_collision(self, other):
        if self.path == [[0, 0]]:

            if other.attitude == Attitude.friendly:
                self.colorup(ds=1)
                self.set_path(movements.make_happy)
            else:
                self.set_path(movements.bounce_back)
