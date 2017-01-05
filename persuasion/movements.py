import random

import game
import utils


def idle(agent):
    return [[0,0]]


def do_nothing(agent):

    return agent.path


def default(agent):
    if agent.step == len(agent.path):
        return agent.default_movement(agent)   ### ??? not sure if the (agent) is needed


def bounce_back(agent, size=6):
    return [map(lambda x: -x, agent.speed)] * size


def make_happy(agent):
    path = [[1,1]] * 3
    path.extend([[-1,1]] * 3)
    path.extend([[-1,-1]] * 3)
    path.extend([[1,-1]] * 3)
    return path


def avoid(agent):
    direction = agent.direction_to(game.main_game.player.rect)
    #agent.speed = [int(round(dir / agent.distance_to_player)) for dir in direction]
    agent.goal = direction
    return path_direct(agent)


def follow(agent):
    pos = utils.random_point_circle(50, game.main_game.player.rect.center)
    agent.goal = pos
    return random_to_goal(agent)


def move_path(agent):
    if agent.step >= len(agent.path):
        if agent.default_movement == side_to_side:
            agent.set_path(agent.default_movement)
            agent.event = False
    try:
        this_move = agent.path[agent.step]
    except IndexError:
        agent.set_path(agent.default_movement)
        this_move = agent.path[agent.step]

    new_x = agent.rect.centerx + this_move[0] * agent.speed_modificator

    if (game.screen_width) >= new_x >= (agent.rect.width/2):
        agent.move(this_move)
    else:
        agent.move([0, this_move[1]])

    agent.step += 1


def circle(agent, size=20):
    path = [[0,1]]*size
    path.extend([[-1,0]]*size)
    path.extend([[0,-1]]*size)
    path.extend([[1,0]]*size)
    return path


def path_direct(agent):
    dx, dy = agent.goal
    path = []
    signdx = -1 if dx < 0 else 1 if dx > 0 else 0
    signdy = -1 if dy < 0 else 1 if dy > 0 else 0

    ddxdy = max(abs(dx),abs(dy)) - min(abs(dx),abs(dy))
    direction = [signdx,0] if abs(dx) > abs(dy) else [0,signdy] if abs(dy) > abs(dx) else [0,0]

    while dx != 0 and dy != 0:
        if ddxdy > 0 and random.randint(1,ddxdy) != 1:
            path.extend([direction])

            dx -= direction[0]
            dy -= direction[1]
        else:
            path.extend([[signdx,signdy]])
            dx -= signdx
            dy -= signdy
    if dx != 0:
        path.extend([[signdx,0]]*abs(dx))
    if dy != 0:
        path.extend([[0,signdy]]*abs(dy))
    return path


def side_to_side(agent):
    max = game.screen_width
    agent_right = agent.rect.right
    agent_left = agent.rect.left

    if agent_left <= 0:
        return [[1, 0]] * (max + agent_left)
    if agent_right >= max:
        return [[-1, 0]] * (max - agent.width)

    if agent_right < max/2:
        return [[-1,0]] * (agent_right)
    else:
        return [[1,0]] * (max - agent_right)


def random_to_goal(agent):
    begin = agent.rect.center
    end = agent.goal
    path = []
    dx = end[0] - begin[0]
    dy = end[1] - begin[1]
    signdx = -1 if dx < 0 else 1 if dx > 0 else 0
    signdy = -1 if dy < 0 else 1 if dy > 0 else 0

    while dx != 0 and dy != 0:
        if random.randint(1,2) == 1:
            path.extend([[signdx,0]])
            dx -= signdx
        else:
            path.extend([[0,signdy]])
            dy -= signdy
    if dx != 0:
        path.extend([[signdx,0]]*abs(dx))
    if dy != 0:
        path.extend([[0,signdy]]*abs(dy))

    if not path:
        # path = [[0,0]]
        path = agent.path

    return path
