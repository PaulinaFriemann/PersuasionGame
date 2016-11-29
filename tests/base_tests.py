from nose.tools import *
from persuasion.main import *
from pygame import Rect

agent = Agent(5, 5, 0)


def test_basic():
    assert_equal(agent.get_rect(), Rect(2, 2, 6, 6))


def test_change():
    agent.set_rect(Rect(0, 0, 6, 6))
    assert_equal(agent.get_rect(), Rect(0,0,6,6))