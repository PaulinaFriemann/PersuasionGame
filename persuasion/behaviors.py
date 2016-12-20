import math


def do_nothing(agent):
    pass


def make_happy(agent):
    pass


def avoid(agent):
    if not agent.runaway and agent.distance_to_player <= agent.personalspace:
        agent.runaway = True
        direction = agent.sensor.direction(agent.player.rect)
        print direction
        agent.speed = [int(round(dir / agent.distance_to_player)) for dir in direction]
        print agent.speed
    agent.move(agent.speed)
