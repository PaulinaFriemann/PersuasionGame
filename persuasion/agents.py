import pygame

import game
import movements
import settings
from enum import Enum

Attitude = {'neutral': 0, 'avoiding': 1, 'friendly': 2, 'friends': 3}


collision_reactions = [movements.bounce_back, movements.bounce_back, movements.make_happy, movements.bounce_back]
personal_space_reactions = [movements.default, movements.avoid, movements.do_nothing, movements.make_happy]


class Agent:
    def __init__(self, x, y, happiness, movement=movements.idle, attitude=Attitude["neutral"]):
        self.happiness = happiness

        self.color = pygame.Color('black')
        self.color.hsva = (260 - (self.happiness * 2),0,90,100)

        self.speed = [0, 0]
        self.width = 10
        self.rect = pygame.Rect(x - self.width / 2, y - self.width / 2, self.width, self.width)
        self.speed_modificator = 1
        self.personalspace = self.width*4
        self.default_movement = movement
        self.attitude = attitude
        self.distance_to_player = 999
        self.path = [[0,0]]
        self.step = 0
        self.event = False
        self.goal = None
        self.s = pygame.Surface((self.width, self.width))
        self.s.fill(self.color)
        self.alpha = 255
        self.s.set_alpha(self.alpha)
        self.fadeaway = False

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
        if self.fadeaway:
            self.fade_away()

    def update_color(self,player_happiness):
        self.color.hsva = (260 - (self.happiness * 2), player_happiness, 90, 0)
        self.s.fill(self.color)
        self.s.set_alpha(self.alpha)

    def set_path(self, movement, default=False, step=0):
#        print movement(self)
        self.step = step
        self.path = movement(self)
        if default:
            self.default_movement = movement

    def set_default_path(self, movement):
        self.default_movement = movement

    def fade_away(self):
        self.alpha -= 1
        if self.alpha < 5:
            game.main_game.agents.remove(self)
        self.s.set_alpha(self.alpha)

    def change_happiness(self, delta):

        self.happiness = max(0, min(self.happiness + delta, 100))
        self.update_color(game.main_game.player.happiness)


    def on_enter_personal_space(self,player):
        if not self.event:

            if self.attitude == Attitude["avoiding"]:
                self.fadeaway = True
                self.set_default_path(movements.do_nothing)
                if (player.happiness > 1): player.happiness -= 1

            self.set_path(personal_space_reactions[self.attitude])


            self.event = True

    def on_collision(self, other):

        print "collision"

        self.set_path(collision_reactions[self.attitude])

        self.event = True

        if self.attitude == Attitude["friendly"]:
            game.main_game.action_queue.add(self.change_attitude, {"attitude": Attitude["friends"]}, len(self.path))
            try:
                game.main_game.action_queue.add(self.set_path, {"movement": movements.follow, "default": True},
                                      len(self.path))
            except TypeError:
                game.main_game.action_queue.add(self.set_path,
                                      {"movement": movements.follow, "default": True},
                                      len(self.path))

    def change_attitude(self, attitude):
        if attitude != self.attitude:
            self.attitude = attitude

class Player(Agent):
    def __init__(self, x, y, happiness):

        Agent.__init__(self, x, y, happiness)
        self.name_area = pygame.Rect(self.rect.left, self.rect.top + 7, 30, 15)

        self.speed_modificator = 1.5

    def move(self, speed):
        self.speed = map(lambda x: self.speed_modificator * x, speed)

        new_x = self.rect.bottomright[0] + self.speed[0]
        if game.screen_width > new_x > (0 + self.rect.width):
            self.rect = self.rect.move(self.speed)

            self.name_area = self.name_area.move(self.speed)
        else:
            self.rect = self.rect.move([0, self.speed[1]])
            self.name_area.move_ip([0, self.speed[1]])

    def update(self):
        if self.path == [[0, 0]]:
            self.move(self.speed)
        else:
            movements.move_path(self)
        #self.update_color()

    def update_color(self,doweneedthis=False):
        #print min(255,max(0,260 - (self.happiness * 2)))
        try:
            self.color.hsva = (min(255,max(0,260 - (self.happiness * 2))), self.happiness, 90, 0)
        except ValueError:
            print (min(255,max(0,260 - (self.happiness * 2))), self.happiness, 90, 0)
        self.s.fill(self.color)

    def on_enter_personal_space(self):
        pass

    def on_bounce(self, other_attitude):
        self.step = 0
        size = 6 if other_attitude == Attitude["friends"] else 10
        self.path = movements.bounce_back(self, size)

    def on_collision(self, other):
        if self.path == [[0, 0]]:
            if other.attitude == Attitude["friendly"]:
                self.change_happiness(5)
                other.change_happiness(5)
                self.set_path(movements.make_happy)
            elif other.attitude != Attitude["friends"]:
                self.change_happiness(-5)
                other.change_happiness(-5)
                self.on_bounce(other.attitude)
