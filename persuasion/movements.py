import random
import agents


def idle(agent):
    return [[0,0]]


def do_nothing(agent):
    pass


def default(agent):
    if agent.step == len(agent.path):
        return agent.defaultpath


def bounce_back(self):
    return [map(lambda x: -x, self.speed)] * 15


def make_happy(agent):
    agent.invoke_attitude = agents.Attitude.friends
    path = [[1,1]] * 3
    path.extend([[-1,1]] * 3)
    path.extend([[-1,-1]] * 3)
    path.extend([[1,-1]] * 3)
    return path


def avoid(agent):
    direction = agent.direction_to(agent.player.rect)
    #agent.speed = [int(round(dir / agent.distance_to_player)) for dir in direction]
    return path_direct(direction)


def follow(agent):
    pass


def move_path(agent):
    if agent.step == len(agent.path):
        agent.event()
        agent.path = agent.defaultpath
        agent.step = 0
    this_move = agent.path[agent.step]
    new_x = agent.rect.centerx + this_move[0] * 2

    if agent.screen.get_width() > new_x > (0 + agent.rect.width):
        agent.move(this_move)
    else:
        agent.move([0, this_move[1]])

    agent.step += 1


def circle(size):
    path = [[0,1]]*size
    path.extend([[-1,0]]*size)
    path.extend([[0,-1]]*size)
    path.extend([[1,0]]*size)
    return path


def path_direct(goal):
    dx, dy = goal
    path = []
    signdx = -1 if dx < 0 else 1 if dx > 0 else 0
    signdy = -1 if dy < 0 else 1 if dy > 0 else 0

    ddxdy = max(abs(dx),abs(dy)) - min(abs(dx),abs(dy))
    direction = [signdx,0] if abs(dx) > abs(dy) else [0,signdy] if abs(dy) > abs(dx) else [0,0]

    while(dx != 0 and dy != 0):
        if ddxdy > 0 and random.randint(1,ddxdy) != 1:
            path.extend([direction])
            #print direction

            dx = dx - direction[0]
            dy = dy - direction[1]
        else:
            path.extend([[signdx,signdy]])
            dx = dx - signdx
            dy = dy - signdy
    if dx > 0:
        path.extend([[signdx,0]]*abs(dx))
    if dy > 0:
        path.extend([[0,signdy]]*abs(dy))
    return path


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
            dx = dx - signdx
        else:
            path.extend([[0,signdy]])
            dy = dy - signdy
    if dx > 0:
        path.extend([[signdx,0]]*abs(dx))
    if dy > 0:
        path.extend([[0,signdy]]*abs(dy))
    return path
