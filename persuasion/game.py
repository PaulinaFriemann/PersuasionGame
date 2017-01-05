import math
import sys
import paulicluster
import pygame
from pygame import Rect

import agents
import gui
import utils
from camera import Camera


def init(width, height):
    global screen_height, screen_width, main_game, screen, player_name
    screen_height = height
    screen_width  = width

    screen = pygame.display.set_mode([screen_width, screen_height])

    player_name = start_screen()
    main_game = Game(600)

    main_game.start()


def start_screen():
    start_screen = gui.StartScreen(screen)
    return start_screen.start()


class Game:

    def __init__(self, end_height):

        self.agents = []
        self.end = end_height
        self.background = gui.Background("resources/snowbig.jpg", [0, 0], screen.get_width(), screen.get_height())
        self.camera = Camera(screen.get_width(), screen.get_height(), self, screen)
        self.player = None
        self.add_player(agents.Player(screen_width / 2, screen_height / 2, 100))
        self.width = screen.get_width()
        self.screen = screen

        self.action_queue = utils.ActionQueue()

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_player(self, player):
        self.agents.append(player)
        self.player = player

    def add_clusters(self, clusters):
        for cluster in clusters:
            for position in cluster.starting_positions:
                agent = agents.Agent(position[0], position[1], 0, attitude=cluster.attitude)
                self.add_agent(agent)

    def load_agents(self):
        clusters = paulicluster.load_all()
        self.add_clusters(clusters)

    def distance(self, rect1, rect2):
        return math.sqrt((rect1.centerx - rect2.centerx) ** 2 + (rect1.centery - rect2.centery) ** 2)

    def start(self):

        self.load_agents()

        self.camera.bar.pop_up()

        clock = pygame.time.Clock()
        while True:
            clock.tick(30)

            pressed = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT \
                        or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            self.player.speed = [int(pressed[pygame.K_RIGHT]) - int(pressed[pygame.K_LEFT]),
                            int(pressed[pygame.K_DOWN]) - int(pressed[pygame.K_UP])]

            self.update()

            pygame.display.flip()

    def update(self):

        self.action_queue.step()

        self.update_agents()
        self.update_agents_color()

        self.camera.move(self.player.speed)

        self.camera.draw()
        self.camera.bar.draw(self.screen)
        pygame.display.flip()

    def update_agents(self):

        for agent in self.agents:
            agent.distance_to_player = self.distance(self.player.rect, agent.rect)
            if not isinstance(agent, agents.Player):
                if agent.distance_to_player <= agent.width:
                    self.player.on_collision(agent)
                    agent.on_collision(self.player)
                if agent.distance_to_player <= agent.personalspace:

                    if (self.player.happiness > 0) and agent.attitude == agents.Attitude["avoiding"]:
                        self.player.change_happiness(-0.5)
                    agent.on_enter_personal_space(self.player)


            agent.update()

    def update_agents_color(self):
        for i in range(len(self.agents)):
            self.agents[i].update_color(self.player.happiness)

    def check_close(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT \
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
