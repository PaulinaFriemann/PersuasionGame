from collections import deque
import pygame
import random
import math


class ActionQueue:

    def __init__(self):
        self.immediate = []
        self.to_invoke = deque()

    def add(self, func, args, frames):
        if frames <= 0:
            self.immediate.append([func, args])
        else:
            if len(self.to_invoke) - 1 < frames:
                for i in range(max(0, len(self.to_invoke) - 1), frames):
                    self.to_invoke.append([])
                self.to_invoke.append([[func,args]])
            else:
                self.to_invoke[frames].append([func, args])

        #print self.to_invoke

    def step(self):
        #print self.to_invoke
        if len(self.to_invoke):
            next_actions = self.to_invoke.popleft()
            for action in next_actions:
                self.immediate.append(action)

        #if self.immediate: print self.immediate

        for action in self.immediate:
            if action:
                action[0](**action[1])

        self.immediate = []


def get_rect(x, y, width, height):
    return pygame.Rect(x - width / 2,
                       y - height / 2,
                       width, height)


def distance(rect1, rect2):
    return math.sqrt((rect1.centerx - rect2.centerx) ** 2 + (rect1.centery - rect2.centery) ** 2)


def center_rect(inner, outer):
    new_top = outer.top + (outer.height/2 - inner.height/2)
    new_left = outer.left + (outer.width/2 - inner.width/2)
    new_rect = pygame.Rect(new_left, new_top, inner.width, inner.height)
    return new_rect


def center_h(inner, outer):
    new_left = outer.left + (outer.width / 2 - inner.width)
    new_rect = pygame.Rect(new_left, inner.top, inner.width, inner.height)
    return new_rect


def random_point_circle(radius, position):
    offset = random.randint(3, radius)
    angle = random.random() * 2 * math.pi
    x = int(position[0] + math.cos(angle) * offset)
    y = int(position[1] - (math.sin(angle) * offset))
    return x,y
