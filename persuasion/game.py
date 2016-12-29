import pygame
from pygame import Rect
import agents
from pygame import freetype
import math
import utils
import gui
import sys


class Game:

    def __init__(self, agents, screen, end_height, top_camera=0, left_camera=0):

        self.agents = agents
        self.end = end_height
        self.background = gui.Background("resources/snowbig.jpg", [0, 0], screen.get_width(), screen.get_height())
        self.camera = Camera(screen.get_width(), screen.get_height(), self, screen, top_camera, left_camera)
        self.player = None
        self.width = screen.get_width()
        self.screen = screen

        self.action_queue = utils.ActionQueue()

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

        self.check_close()

        self.action_queue.step()

        self.update_agents()

        self.camera.move(self.player.speed)

        self.camera.draw()
        pygame.display.flip()

    def update_agents(self):

        for agent in self.agents:
            agent.distance_to_player = self.distance(self.player.rect, agent.rect)
            if not isinstance(agent, agents.Player):
                if agent.distance_to_player <= 6:
                    self.player.on_collision(agent)
                    agent.on_collision(self.player)
                if agent.distance_to_player <= agent.personalspace:
                    agent.on_enter_personal_space()

            agent.update()

    def check_close(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT \
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def start_screen(self):

        start_button = gui.Button(270, 342, 100, 30)
        start_button.set_text("Start Game")

        text_area = gui.TextArea(15, utils.center_rect(Rect(0,0,200,30), self.screen.get_rect()))
        started = False
        while not started:

            for event in pygame.event.get():
                if event.type == pygame.QUIT \
                        or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos, button = event.pos, event.button
                    if start_button.collidepoint(*pos):
                        started = True
                if event.type == pygame.KEYUP:
                    if pygame.K_a <= event.key <= pygame.K_z:
                        text_area.add_letter(pygame.key.name(event.key))
                    elif event.key == pygame.K_BACKSPACE:
                        text_area.delete_letter()

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
        self.bar = gui.NarratorBar(15, Rect(0, 350, self.width, self.height))

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
        self.world.background.draw(self.screen, self.position)

        for agent in self.world.agents:
            if self.check_visibility(agent.rect):
                new_rect = self.adjust(agent)
                pygame.draw.rect(self.screen, agent.color, new_rect)

        self.draw_overlay()
        self.bar.draw(self.screen)

    def draw_overlay(self, alpha=20):

        s = pygame.Surface((640, 480))  # the size of your rect
        s.set_alpha(alpha)  # alpha level
        s.fill((0, 0, 0))  # this fills the entire surface
        self.screen.blit(s, (0, 0))  # (0,0) are the top-left coordinates
