import math
import movements


def do_nothing(agent):
    pass


def make_happy(agent):
    if agent.rect.colliderect(agent.player.rect):
        agent.player.colorup(ds=0.1)


def avoid(agent):
    dist = agent.sensor.distance(agent.player.rect)
    print dist
    if not agent.runaway and dist <= agent.personalspace:
        agent.runaway = True
        direction = agent.sensor.direction(agent.player.rect)
        print direction
        agent.speed = [dir / dist for dir in direction]
        print agent.speed
    agent.path = path_direct(direction)
