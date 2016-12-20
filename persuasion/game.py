import pygame
from pygame import Rect
import agents
from pygame import freetype


def get_rect(x, y, width, height):
    return pygame.Rect(x - width / 2,
                       y - height / 2,
                       width, height)
        

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
        return Rect(new_left, new_top, agent.rect.width, agent.rect.height)

    def check_visibility(self, rect):
        return self.position.contains(rect)

    def draw(self):
        self.draw_background()

        for agent in self.world.agents:
            if self.check_visibility(agent.rect):
                new_rect = self.adjust(agent)
                pygame.draw.rect(self.screen, agent.color, new_rect)
                if not isinstance(agent, agents.Player):
                    agent.sensor.update(agent.rect)
                    pygame.draw.circle(self.screen, pygame.Color("White"), new_rect.center, agent.sensor.radius)

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
