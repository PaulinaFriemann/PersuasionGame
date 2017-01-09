import random

import game
import utils


def idle(agent):
    return [[0,0]]


def do_nothing(agent):
    if not agent.path:
        return default(agent)
    return agent.path


def default(agent):
    if agent.default_movement != do_nothing:
        return agent.default_movement(agent)   ### ??? not sure if the (agent) is needed
    else:
        return idle(agent)


def bounce_back(agent, size=6):
    return [map(lambda x: -x, agent.speed)] * size


def make_happy(agent):
    path = [[1,-1]] * 5
    path.extend([[0,0]] * 3)
    path.extend([[-1,1]] * 5)
    path.extend([[0,0]] * 3)
    path.extend([[-1,-1]] * 5)
    path.extend([[0,0]] * 3)
    path.extend([[1,1]] * 5)
    path.extend([[0,0]] * 3)
    path.extend([[0,-1]] * 5)
    path.extend([[0,0]] * 3)
    path.extend([[0,1]] * 5)
    path.extend([[0,0]] * 3)
    path.extend([[0,-1]] * 5)
    path.extend([[0,0]] * 3)
    path.extend([[0,0],[0,0],[0,1]] * 5)
    return path

def happy_dance(agent):
    path = [[-1,-1]] * 4
    path.extend([[1,1]] * 4)
    path.extend([[1,-1]] * 4)
    path.extend([[-1,1]] * 4)
    path.extend([[0,-1]] * 4)
    path.extend([[0,1]] * 4)
    path.extend([[0,-1]] * 4)
    path.extend([[0,0]] * 10)
    return path

def avoid(agent):
    direction = agent.direction_to(game.main_game.player.rect)
    #agent.speed = [int(round(dir / agent.distance_to_player)) for dir in direction]
    agent.goal = direction
    print "avoid ", direction
    return path_direct(agent)

def follow(agent):
    pos = utils.random_point_circle(25 + int(agent.runaway), game.main_game.player.rect.center)
    agent.goal = pos
    print pos
    return random_to_goal(agent)[:5]


def move_path(agent):
    if(agent.frozen): pass
    else:
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
        if not agent.fadeaway:
            if game.screen_width >= new_x >= (agent.rect.width/2):
                agent.move(this_move)
            else:
                agent.move([0, this_move[1]])
        else:
            agent.move(this_move)

        agent.step += 1

def circle_around(agent, (center_x, center_y), radius = 20):
    beginx = agent.rect.centerx
    beginy = agent.rect.centery




def circle(agent, size=40):
    path = [[0,0], [0,1], [0,0]]*(size/2)
    path.extend([[0, 0], [-1, 1], [0, 0]] * (size / 2))
    path.extend([[0,0], [-1,0], [0,0]]*(size/2))
    path.extend([[0, 0], [-1, -1], [0, 0]] * (size / 2))
    path.extend([[0,0], [0,-1], [0,0]]*(size/2))
    path.extend([[0, 0], [1, -1], [0, 0]] * (size / 2))
    path.extend([[0,0], [1,0], [0,0]]*(size/2))
    path.extend([[0,0], [1,1], [0,0]]*(size/2))
    return path


def rand_circle(agent,min_r = 30, max_r = 60):
    size = random.randint(min_r, max_r)

    return circle(agent, size)


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
    max = 500#game.screen_width
    agent_right = agent.rect.right
    agent_left = agent.rect.left

    rand = random.randint(0,2)

    if agent_left <= 0:
        return [[1, 0]] * (max + agent_left)
    if agent_right >= max:
        return [[-1, 0]] * (max - agent.width)

    if rand == 1:
        return [[-1,0]] * agent_right
    else:
        return [[1,0]] * (max - agent_right)


def from_to_rand(agent):
    if agent.goal == agent.goal_a:
        agent.goal = agent.goal_b
    else:
        agent.goal = agent.goal_a
    return random_to_goal(agent)


def path(agent):

    end_x, end_y = agent.goal



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
            path.extend([[0,0], [signdx,0], [0,0]])
            dx -= signdx
        else:
            path.extend([[0,0], [0,signdy], [0,0]])
            dy -= signdy
    if dx != 0:
        path.extend([[0,0], [signdx,0], [0,0]]*abs(dx))
    if dy != 0:
        path.extend([[0,0], [0,signdy], [0,0]]*abs(dy))

    if not path:
        # path = [[0,0]]
        path = agent.path

    return path
