import pygame
from pygame import Rect


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

    def move(self):
        self.speed = map(lambda x: 2*x, self.speed)
        new_x = self.rect.bottomright[0] + self.speed[0]
        if self.screen.get_width() > new_x > (0 + self.width):
            self.rect = self.rect.move(self.speed)
        else:
            self.rect = self.rect.move([0, self.speed[1]])

    def colorup(self, dh = 0,ds = 0,dv = 0):
        h,s,v,a = self.color.hsva
        if h + dh <= 255 and s + ds <= 100 and v + dv <= 100:
            self.color.hsva = (h+dh,s+ds,v+dv,a)

    def update(self):
        self.move()


class Game:

    def __init__(self, agents, screen, end_height, top_camera=0, left_camera=0):

        self.agents = agents
        self.end = end_height
        self.background = Background("resources/pic.jpg", [0, -120])
        self.camera = Camera(screen.get_width(), screen.get_height(), self, screen, top_camera, left_camera)
        self.player = None
        self.width = screen.get_width()

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_player(self, player):
        self.agents.append(player)
        self.player = player
        self.camera.calibrate(player)

    def update(self):

        for agent in self.agents:
            agent.update()

        self.camera.move(self.player.speed)
        self.camera.draw()
        pygame.display.flip()


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
        new_left = self.position.left + player_speed[0]
        new_right = self.position.right + player_speed[0]

        if new_left < 0:
            self.position.left = 0

        elif new_right > self.world.width:
            self.position.right = self.width

        else:
            self.position.left += player_speed[0]

        self.position.top += player_speed[1]

    def adjust(self, agent):
        new_left = agent.rect.left - self.position.left
        new_top = agent.rect.top - self.position.top

        return Rect(new_left, new_top, agent.width, agent.height)

    def check_visibility(self, rect):
        return self.position.contains(rect)

    def draw(self):

        self.screen.fill([0, 0, 0])
        blit_position = Rect(-self.position.left, -self.position.top, self.position.width, self.position.width)
        self.screen.blit(self.world.background.image, blit_position)
        for agent in self.world.agents:
            if self.check_visibility(agent.rect):
                pygame.draw.rect(self.screen, agent.color, self.adjust(agent))


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location