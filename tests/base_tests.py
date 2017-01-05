import math

from nose.tools import *

from persuasion.utils import *
from persuasion.paulicluster import *
from pprint import pprint
from persuasion.agents import Attitude
from enum import Enum


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


    assert True


def hello():
    print "hello"


def hello2(a, b):

    print "hello ", a, b


def test_action_queue():
    queue = ActionQueue()
    queue.add(hello, {}, 2)

    #assert_equals(queue.immediate, [[hello, {}]])

    queue.add(hello2, {"a":"a", "b":"b"}, 2)

    assert_equals(queue.to_invoke, deque([[], [], [[hello, {}],[hello2, {"a":"a", "b":"b"}]]]))

    #assert_equals(queue.immediate, [[hello, {}], [hello2, {"a":"a", "b":"b"}]])

    queue.step()

    queue.step()

    queue.step()

   # assert False


def test_cluster():
    init_dict = {'number': 0, 'num_agents': 0, 'attitude': Attitude.friendly, 'positions':[[]]}
    cluster1 = PauliCluster(number=1, num_agents=1, attitude=Attitude.friendly, positions=[[20,20], [34,123]])
    cluster1.move(10,0)
    print cluster1

    assert False


def test_enum():
   # enuma = Enum({'red': 20, 'orange': 10, 'green': 0})
   # print enuma(10)

    assert True
