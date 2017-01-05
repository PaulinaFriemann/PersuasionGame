import math
import sys
import cluster
import pygame
from pygame import Rect

import agents
import gui
import utils
import movements
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
        self.clusters = []
        self.end = end_height
        self.background = gui.Background("resources/snowbig.jpg", [0, 0], screen.get_width(), screen.get_height())
        self.camera = Camera(screen.get_width(), screen.get_height(), self, screen)
        self.player = None
        self.add_player(agents.Player(screen_width / 2, screen_height / 2, 50))
        self.width = screen.get_width()
        self.screen = screen
        self.in_editor_mode = False

        self.music = None#pygame.mixer.music.load("resources/")

        self.last_cluster = []

        self.action_queue = utils.ActionQueue()

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_player(self, player):
        self.agents.append(player)
        self.player = player

    def add_clusters(self, clusters):
        for cluster in clusters:
            self.clusters.append(cluster)
            for position in cluster.starting_positions:
                agent = agents.Agent(position[0], position[1], 0, attitude=cluster.attitude)
                self.add_agent(agent)

        for agent in self.agents[1:2]:
            agent.set_path(movements.side_to_side,default=True)

    def load_agents(self):
        clusters = cluster.load_all()
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
                    #paulicluster.save_all(self.clusters)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP and event.key == pygame.K_BACKSPACE:
                    self.in_editor_mode = not self.in_editor_mode

            if not self.in_editor_mode:
                self.player.speed = [int(pressed[pygame.K_RIGHT]) - int(pressed[pygame.K_LEFT]),
                                int(pressed[pygame.K_DOWN]) - int(pressed[pygame.K_UP])]

                self.update()

            else:
                self.editor_mode()

            pygame.display.flip()

    def editor_mode(self):
        block = 0
        clock = pygame.time.Clock()
        agent_pos = []
        num_clusters = len(self.clusters)

        attitude = agents.Attitude["avoiding"]

        while self.in_editor_mode:
            clock.tick(30)
            mousepressed = pygame.mouse.get_pressed()[0] if block == 0 else False

            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_1:
                        print "Attitude is now avoiding"
                        attitude = agents.Attitude["avoiding"]
                    elif event.key == pygame.K_2:
                        print "Attitude is now neutral"
                        attitude = agents.Attitude["neutral"]
                    elif event.key == pygame.K_3:
                        print "Attitude is now friendly"
                        attitude = agents.Attitude["friendly"]
                    elif event.key == pygame.K_4:
                        print "Attitude is now friends"
                        attitude = agents.Attitude["friends"]

                if event.type == pygame.KEYUP and event.key == pygame.K_z:
                    print self.clusters.pop()
                    agent_pos = self.last_cluster

                if event.type == pygame.QUIT \
                        or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    if len(agent_pos):
                        num_clusters += 1

                        #

                        new_cluster = cluster.Cluster(number=num_clusters, attitude=attitude,
                                                                starting_positions=[list(pos.center) for pos in agent_pos])
                        cluster.append_to_end(new_cluster)



                if event.type == pygame.KEYUP and event.key == pygame.K_BACKSPACE:
                    if len(agent_pos):
                        num_clusters += 1

                        new_cluster = cluster.Cluster(number=num_clusters, attitude=attitude,
                                                                starting_positions=[list(pos.center) for pos in agent_pos])
                        self.clusters.append(new_cluster)

                        cluster.append_to_end(new_cluster)
                        new_cluster.add_cluster(game = self)
                    self.last_cluster = agent_pos
                    self.in_editor_mode = False

            if mousepressed:

                position = list(pygame.mouse.get_pos())
                print position, self.camera.position.top
                position[1] += self.camera.position.top
                print position
                rect = utils.get_rect(position[0], position[1], 10, 10)
                if any([rect.colliderect(other) for other in agent_pos]):
                    colliders = filter(rect.colliderect, agent_pos)
                    for col in colliders:
                        agent_pos.remove(col)
                else:
                    agent_pos.append(rect)
                block = 10

            block = max(0, block - 1)

            self.camera.draw()

            for pos in agent_pos:
                pygame.draw.rect(self.screen, pygame.Color("Black"), pos.move([0,-self.camera.position.top]))

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
