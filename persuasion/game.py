import pygame
import random
from pygame import Rect
<<<<<<< HEAD
=======
from pygame import freetype
import math
>>>>>>> origin/master


def get_rect(x, y, width, height):
    return pygame.Rect(x - width / 2,
                       y - height / 2,
                       width, height)

<<<<<<< HEAD
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
        

class Agent:

    def __init__(self, x, y, color, screen):
        self.width = 6
        self.height = 6
        self.color = color
        self.image = pygame.Surface((self.width,self.height))
        self.speed = [0,0]
        self.screen = screen
        self.rect = pygame.Rect(x - self.width/2, y - self.height/2, self.width, self.height)
        self.location = [x, y]
        self.personalspace = 10
        self.path = path_circle(40)
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

    def update(self):
        self.move()

class Player(Agent):
    def __init__(self, x, y, color, screen):
        self.width = 6
        self.height = 6
        self.color = color
        self.image = pygame.Surface((self.width,self.height))
        self.speed = [0,0]
        self.screen = screen
        self.rect = pygame.Rect(x - self.width/2, y - self.height/2, self.width, self.height)
        self.location = [x, y]
        self.step = 0

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


=======
>>>>>>> origin/master

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
        self.bar = pygame.image.load("resources/bar.jpg")

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

        self.draw_overlay()
        self.draw_bar()

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

    def draw_overlay(self, alpha=20):

        s = pygame.Surface((640, 480))  # the size of your rect
        s.set_alpha(alpha)  # alpha level
        s.fill((0, 0, 0))  # this fills the entire surface
        self.screen.blit(s, (0, 0))  # (0,0) are the top-left coordinates

    def draw_bar(self):
        self.bar.set_alpha(100)  # alpha level

        self.write_text()

        self.screen.blit(self.bar, (0, 350))  # (0,0) are the top-left coordinates

    def write_text(self):
        font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 15)
        rect = self.center(font.get_rect("Hallo wie gehts?"))
        label = font.render_to(self.bar, rect.center,"Hallo wie gehts?")

    def center(self, rect):
        return rect.move([self.width/2 - rect.width, 20])


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        print self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
