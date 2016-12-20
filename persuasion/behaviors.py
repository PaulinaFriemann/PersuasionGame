import math
import movements


def do_nothing(agent):
    pass


def make_happy(agent):
    pass


def avoid(agent):
    if agent.distance_to_player <= agent.personalspace:
        direction = agent.sensor.direction(agent.player.rect)
        agent.path = movements.path_direct([x * 3 for x in direction])
        agent.step = 0