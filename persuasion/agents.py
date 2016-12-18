import pygame


def path_circle(size):
    path = [[0,1]]*size
    path.extend([[-1,0]]*size)
    path.extend([[0,-1]]*size)
    path.extend([[1,0]]*size)
    return path


class Agent:
    def __init__(self, x, y, color, screen):
        self.width = 6
        self.height = 6
        self.color = color
        self.image = pygame.Surface((self.width, self.height))
        self.speed = [0, 0]
        self.screen = screen
        self.rect = pygame.Rect(x - self.width / 2, y - self.height / 2, self.width, self.height)
        self.speed_modificator = 2

        self.sensor = pygame.Rect(x - self.width / 2, y - self.height / 2, self.width * 3, self.height * 3)

    def move_speed(self, speed):
        self.rect = self.rect.move(speed)
        self.sensor = self.sensor.move(speed)

    def move(self):
        self.speed = map(lambda x: self.speed_modificator * x, self.speed)
        self.rect = self.rect.move(self.speed)

        self.sensor = self.sensor.move(self.speed)

    def update(self):
        self.move()


class AvoidantAgent(Agent):
    def __init__(self, x, y, color, screen, player):
        Agent.__init__(self, x, y, color, screen)
        self.player = player
        self.speed_modificator = 1
        self.runaway = False

    def update(self):
        if not self.runaway and self.sensor.colliderect(self.player.rect):
            self.runaway = True
            self.speed = self.player.speed

        self.move()


class MarcsAgent(Agent):
    def __init__(self, x, y, color, screen):
        Agent.__init__(self, x, y, color, screen)
        self.location = [x, y]
        self.path = path_circle(20)
        self.step = 0
        self.turn = 0

    def move(self):
        if (self.turn == 0):
            self.turn = 1
        else:
            if (self.step == len(self.path)): self.step = 0
            this_move = self.path[self.step]
            new_x = self.location[0] + this_move[0] * 2

            if self.screen.get_width() > new_x > (0 + self.width):
                self.rect = self.rect.move(this_move)
            else:
                self.rect = self.rect.move([0, this_move[1]])

            self.step = self.step + 1


class Player(Agent):
    def __init__(self, x, y, color, screen):

        Agent.__init__(self, x, y, color, screen)
        self.location = [x, y]
        self.step = 0
        self.speed_modificator = 3

    def move(self):

        self.speed = map(lambda x: self.speed_modificator * x, self.speed)

        new_x = self.rect.bottomright[0] + self.speed[0]
        if self.screen.get_width() > new_x > (0 + self.width):
            self.rect = self.rect.move(self.speed)
        else:
            self.rect = self.rect.move([0, self.speed[1]])

    def colorup(self, dh=0, ds=0, dv=0):
        h, s, v, a = self.color.hsva
        if h + dh <= 255 and s + ds <= 100 and v + dv <= 100:
            self.color.hsva = (h + dh, s + ds, v + dv, a)
