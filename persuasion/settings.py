from game import Game
import pygame
from enum import Enum


def init(width, height):
    global screen_height, screen_width, game
    screen_height = height
    screen_width  = width

    screen = pygame.display.set_mode([screen_width, screen_height])
    game = Game(screen, 600)
    print screen