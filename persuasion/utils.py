from collections import deque
import pygame


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
                self.to_invoke.append([func,args])
            else:
                self.to_invoke[frames].append([func, args])

    def step(self):
        if len(self.to_invoke):
            next_actions = self.to_invoke.popleft()
            self.immediate.append(next_actions)

        for action in self.immediate:
            if action:
                if action[1]:
                    action[0](*action[1])
                else:
                    action[0]()

        self.immediate = []


def get_rect(x, y, width, height):
    return pygame.Rect(x - width / 2,
                       y - height / 2,
                       width, height)


def center_rect(inner, outer):
    new_top = outer.top + (outer.height/2 - inner.height/2)
    new_left = outer.left + (outer.width/2 - inner.width/2)
    new_rect = pygame.Rect(new_left, new_top, inner.width, inner.height)
    return new_rect


def center_horizontal(rect, outer_width):
    return rect.move([outer_width / 2 - rect.width, 0])