import pygame
from pygame import Rect


WORLD_LENGTH = 500


def get_rect(x, y, width, height):
    return pygame.Rect(x - width / 2,
                       y - height / 2,
                       width, height)


class Agent:

    def __init__(self, x, y, color, screen, player = False):
        self.width = 6
        self.height = 6
        self.player = player
        self.color = color
        self.image = pygame.Surface((self.width,self.height))
        self.speed = [0,0]
        self.screen = screen
        self.rect = pygame.Rect(x - self.width/2, y - self.height/2, self.width, self.height)

    def set_rect(self, rect):
        self.rect = rect

    def move(self, speed):
        speed = map(lambda x: x, speed)
        new_x = self.rect.bottomright[0] + speed[0]
        if self.screen.get_width() > new_x > (0 + self.width):
            self.set_rect(self.rect.move(speed))

    def colorup(self, dh = 0,ds = 0,dv = 0):
        h,s,v,a = self.color.hsva
        if h + dh <= 255 and s + ds <= 100 and v + dv <= 100:
            self.color.hsva = (h+dh,s+ds,v+dv,a)

    def update(self):
        self.move(self.speed)


class World:

    def __init__(self, agents, width, end):
        # [agent, visible]
        #self.agents = [[agent, False] for agent in agents]
        self.agents = agents
        self.width = width
        self.end = end
        self.background = Background("resources/pic.jpg", [0, -120])

    def add_agent(self, agent):
        #self.agents.append([agent, False])
        self.agents.append(agent)

    def draw(self):
        pass


class Camera:

    def __init__(self, width, height, world, screen=None, top=0, left=0):
        self.height = height
        self.width = width
        self.world = world
        self.max_height = world.end
        self.position = Rect(left, top, width, height)
        self.screen = screen

    def calibrate(self, player):
        self.offset = [player.rect.left - self.position.left, player.rect.top - self.position.top]

    def move(self, player_speed):
        self.position.left += player_speed[0]
        self.position.top += player_speed[1]
        print "camera position ", self.position

    def adjust(self, agent):
        new_left = agent.rect.left - self.position.left
        new_top = agent.rect.top - self.position.top

        return Rect(new_left, new_top, agent.width, agent.height)

    def check_visibility(self, rect):
        #print rect
        return rect.left > self.position.left or rect.top > self.position.top \
            or rect.right < self.position.right or rect.bottom > self.position.bottom

    def draw(self):
        for agent in self.world.agents:
            if self.check_visibility(agent.rect):
                print "true value ", agent.rect
                pygame.draw.rect(self.screen, agent.color, self.adjust(agent))
                print "adjusted ", self.adjust(agent)


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location