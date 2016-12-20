import math
import movements


def do_nothing(agent):
    pass


def make_happy(agent):
    pass


def avoid(agent):

    if agent.distance_to_player <= agent.personalspace:
        direction = agent.direction_to(agent.player.rect)
        agent.speed = [int(round(dir / agent.distance_to_player)) for dir in direction]
        agent.path = movements.path_direct(direction)
        agent.step = 0
