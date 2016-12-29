from nose.tools import *
# from persuasion.game import *
# from persuasion.agents import *
# import pygame
# from pygame import Rect
import math


# size = width, height = 640, 480
#
# screen = pygame.display.set_mode(size)
#
# x_player = 50
# y_player = 20
#
# agent = Agent(20, 40, pygame.Color('Pink'), screen)
# agents = [agent]
#
#
# player = Agent(50, 20, pygame.Color('White'), screen)
#
# w = Game(agents, screen, 600)


def distance ((x_1, y_1), (x_2, y_2)):

    dist =  math.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2)
    print "x, y ", (x_2, y_2)
    print "dist ", dist
    return dist


def test_basic():

    diameter = 3
    radius = diameter/2
    dist_arr = [[0.0 for _ in range(diameter)] for _ in range(diameter)]
    arr = [[False for _ in range(diameter)] for _ in range(diameter)]

    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            dist = distance((0.0,0.0), (x,y))
            print "in array pos ", (y+radius, x+radius)
            dist_arr[y + radius][x + radius] = dist
            if dist <= radius:
                try:
                    arr[y + radius][x + radius] = True
                except IndexError:
                    print x + radius, y+ radius


    print dist_arr
    print arr





    assert False
