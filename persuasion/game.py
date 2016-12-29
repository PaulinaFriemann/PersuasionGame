import pygame
from pygame import Rect
import agents
from pygame import freetype
import math
from utils import ActionQueue
import sys


def get_rect(x, y, width, height):
    return pygame.Rect(x - width / 2,
                       y - height / 2,
                       width, height)


def center_rect(inner, outer):
    new_top = outer.top + (outer.height/2 - inner.height/2)
    new_left = outer.left + (outer.width/2 - inner.width/2)
    new_rect = Rect(new_left, new_top, inner.width, inner.height)
    return new_rect


def center(rect, outer_width):
    return rect.move([outer_width / 2 - rect.width, 20])


class Button(Rect):

    def __init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)

    def set_text(self, text):
        self.text = text

        self.font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 15)
        self.text_rect = center_rect(self.font.get_rect(text), self)

    def draw(self, screen):
        pygame.draw.rect(screen, [200,200,200], self)
        self.font.render_to(screen, self.text_rect.topleft,
                           self.text, fgcolor = (150,20,255))


class TextArea(Rect):

    def __init__(self, *args, **kwargs):
        super(TextArea, self).__init__(*args, **kwargs)

        self.font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 15)
        self.text = ""
        self.text_rect = center_rect(self.font.get_rect(self.text), self)

    def add_letter(self, letter):
        self.text += letter
        self.text_rect = center_rect(self.font.get_rect(self.text), self)

    def draw(self, screen):
        pygame.draw.rect(screen, [200,200,200], self)
        self.font.render_to(screen, self.text_rect.topleft,
                           self.text, fgcolor = (150,20,255))



class Game:

    def __init__(self, agents, screen, end_height, top_camera=0, left_camera=0):

        self.agents = agents
        self.end = end_height
        self.background = Background("resources/snowbig.jpg", [0, 0])
        self.camera = Camera(screen.get_width(), screen.get_height(), self, screen, top_camera, left_camera)
        self.player = None
        self.width = screen.get_width()
        self.screen = screen

        self.action_queue = ActionQueue()

    def add_agent(self, agent):
        print "I created an agent <<BEEP>>"
        self.agents.append(agent)

    def add_player(self, player):
        self.agents.append(player)
        self.player = player

    def distance(self, rect1, rect2):
        return math.sqrt((rect1.centerx - rect2.centerx) ** 2 + (rect1.centery - rect2.centery) ** 2)

    def start(self):

            self.start_screen()

    def update(self):

        self.action_queue.step()

        for agent in self.agents:
            agent.distance_to_player = self.distance(self.player.rect, agent.rect)
            if not isinstance(agent, agents.Player):
                if agent.distance_to_player <= 6:
                    self.player.on_collision(agent)
                    agent.on_collision(self.player)
                if agent.distance_to_player <= agent.personalspace:
                    agent.on_enter_personal_space()

            agent.update()

        self.camera.move(self.player.speed)

        self.camera.draw()
        pygame.display.flip()

    def start_screen(self):

        start_button = Button(270, 342, 100, 30)
        start_button.set_text("Start Game")

        text_area = TextArea(center_rect(Rect(0,0,200,30), self.screen.get_rect()))
        started = False
        while not started:
            pressed = pygame.key.get_pressed()
            mousepressed = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT \
                        or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos, button = event.pos, event.button
                    if start_button.collidepoint(*pos):
                        started = True
                if event.type == pygame.KEYDOWN and (pygame.K_a <= event.key <= pygame.K_z):
                    text_area.add_letter(pygame.key.name(event.key))

            self.screen.fill([0,0,0])
            start_button.draw(self.screen)
            text_area.draw(self.screen)
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
        rect = center(font.get_rect("Hallo wie gehts?"), self.width)
        label = font.render_to(self.bar, rect.center,"Hallo wie gehts?")


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        print self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
