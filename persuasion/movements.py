import random


def idle(agent):
    return [0,0]


def circle(agent):
    if agent.step == len(agent.path): agent.step = 0
    this_move = agent.path[agent.step]
    new_x = agent.rect.centerx + this_move[0] * 2

    if agent.screen.get_width() > new_x > (0 + agent.rect.width):
        agent.move(this_move)
    else:
        agent.rect = agent.rect.move([0, this_move[1]])

    agent.step += 1


def path_circle(size):
    path = [[0,1]]*size
    path.extend([[-1,0]]*size)
    path.extend([[0,-1]]*size)
    path.extend([[1,0]]*size)
    return path


def path_route(begin,end):
    path = []
    dx = end[0] - begin[0]
    dy = end[1] - begin[1]
    signdx = -1 if dx < 0 else 1 if dx > 0 else 0
    signdy = -1 if dy < 0 else 1 if dy > 0 else 0

    while(dx != 0 and dy != 0):
        if random.randint(1,2) == 1:
            path.extend([[signdx,0]])
            dx = dx - signdx
        else:
            path.extend([[0,signdy]])
            dy = dy - signdy
    if dx > 0:
        path.extend([[signdx,0]]*abs(dx))
    if dy > 0:
        path.extend([[0,signdy]]*abs(dy))
    return path