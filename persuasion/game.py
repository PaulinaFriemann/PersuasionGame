import pygame
from pygame import Rect
import math

def get_rect(x, y, width, height):
    return pygame.Rect(x - width / 2,
                       y - height / 2,
                       width, height)

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
        self.image = pygame.Surface((self.width,self.height))
        self.speed = [0,0]
        self.screen = screen
        self.rect = pygame.Rect(x - self.width/2, y - self.height/2, self.width, self.height)
        self.speed_modificator = 2

        self.sensor = pygame.Rect(x - self.width/2, y - self.height/2, self.width * 3, self.height * 3)

    def move_speed(self, speed):

        self.rect = self.rect.move(speed)
        self.sensor = self.sensor.move(speed)

    def move(self):

        self.speed = map(lambda x: self.speed_modificator*x, self.speed)
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
            new_x = self.location[0] + this_move[0]*2

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

        self.speed = map(lambda x: self.speed_modificator*x, self.speed)

        new_x = self.rect.bottomright[0] + self.speed[0]
        if self.screen.get_width() > new_x > (0 + self.width):
            self.rect = self.rect.move(self.speed)
        else:
            self.rect = self.rect.move([0, self.speed[1]])
            
    def colorup(self, dh = 0,ds = 0,dv = 0):
        h,s,v,a = self.color.hsva
        if h + dh <= 255 and s + ds <= 100 and v + dv <= 100:
            self.color.hsva = (h+dh,s+ds,v+dv,a)


class Game:

    def __init__(self, agents, screen, end_height, top_camera=0, left_camera=0):

        self.agents = agents
        self.end = end_height
        self.background = Background("resources/snowbig.jpg", [0, 0])
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
        self.draw_background()

        for agent in self.world.agents:
            if self.check_visibility(agent.rect):
                pygame.draw.rect(self.screen, agent.color, self.adjust(agent))

        self.draw_overlay(alpha=128)

    def draw_background(self):
        self.screen.fill([0, 0, 0])
        blit_position = Rect(-self.position.left, 0, self.position.width, self.position.height)

        area_horizontal = self.world.background.rect.width / 2 - self.width / 2
        area_vertical   = (self.world.background.rect.height - self.height + self.position.top) % (-self.world.background.rect.height)

        self.screen.blit(self.world.background.image, blit_position,
                         area=Rect(area_horizontal, area_vertical, self.width, self.height))

        if area_vertical < 0:
            blit_position.height = -area_vertical
            new_area_vertical = self.world.background.rect.height + area_vertical
            self.screen.blit(self.world.background.image, blit_position,
                             area=Rect(area_horizontal, new_area_vertical, self.width, -area_vertical))

    def draw_overlay(self, alpha=0):

        s = pygame.Surface((640, 480))  # the size of your rect
        s.set_alpha(alpha)  # alpha level
        s.fill((0, 0, 0))  # this fills the entire surface
        self.screen.blit(s, (0, 0))  # (0,0) are the top-left coordinates


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        print self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
