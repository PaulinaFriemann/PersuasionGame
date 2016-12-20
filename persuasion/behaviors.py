import math
import movements


def do_nothing(agent):
    pass


def make_happy(agent):
    pass


def avoid(agent):
    if not agent.runaway and agent.distance_to_player <= agent.personalspace:
        agent.runaway = True
        direction = agent.direction_to(agent.player.rect)
        print direction
        agent.speed = [int(round(dir / agent.distance_to_player)) for dir in direction]
        print agent.speed
        agent.path = movements.path_direct(direction)
