from nose.tools import *
from persuasion.game import *
import pygame
from pygame import Rect


size = width, height = 640, 480

screen = pygame.display.set_mode(size)

agent = Agent(20, 40, pygame.Color('Pink'), screen)
agents = [agent]


player = Agent(50, 20, pygame.Color('White'), screen)

w = World(agents, 200, 300)


def test_basic():
    assert_equal(agent.rect, Rect(17, 37, 6, 6))


def test_change():
    agent.set_rect(Rect(0, 0, 6, 6))
    assert_equal(agent.rect, Rect(0,0,6,6))


def test_append():

    w.add_agent(player)
    print w.agents
    #assert_equal(w.agents, [[agent, False], [player, False]])
    assert_equal(w.agents, [agent, player])


def test_move_player():
    player = Agent(50, 20, pygame.Color('White'), screen)

    player.speed = [-1, 0]
    player.update()

    assert_equal(player.rect, get_rect(49, 20, 6, 6))


def test_rect():

    assert_equal(get_rect(10, 10, 6, 10), Rect(7, 5, 6, 10))


def test_move_camera():
    player = Agent(50, 20, pygame.Color('White'), screen)

    player.speed = [2, -5]

    camera = Camera(200, 200, w, screen)
    camera.calibrate(player)

    player.update()

    camera.move(player.speed)

    assert_equal(camera.position, Rect(2, -5, 200, 200))


def test_adjust_camera():
    player = Agent(50, 20, pygame.Color('White'), screen)

    agent = Agent(20, 40, pygame.Color('Pink'), screen)

    camera = Camera(200, 200, w, screen, left=10, top=10)
    camera.calibrate(player)

    assert_equal(camera.adjust(player), Rect(camera.offset[0], camera.offset[1], player.width, player.height))

    assert_equal(camera.adjust(agent), Rect(7, 27, agent.width, agent.height))


def test_move_adjust():
    player = Agent(50, 20, pygame.Color('White'), screen)
    agent = Agent(20, 40, pygame.Color('Pink'), screen)
    camera = Camera(200, 200, w, screen)
    camera.calibrate(player)

    player.speed = [-1,0]

    player.update()

    camera.move(player.speed)

    assert_equal(camera.adjust(player), Rect(camera.offset[0], camera.offset[1], player.width, player.height))
    assert_equal(camera.adjust(agent), get_rect(21,40,6,6))


def test_visibility():
    player = Agent(50, 20, pygame.Color('White'), screen)
    camera = Camera(200, 200, w, screen, left=10, top=10)
    camera.calibrate(player)

    assert_equal(camera.check_visibility(player.rect), True)
    assert_equal(camera.check_visibility(agent.rect), True)

