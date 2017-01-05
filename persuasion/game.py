import math
import sys
import paulicluster
import pygame
from pygame import Rect

import agents
import gui
import utils


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


event_positions = [-500]
event_text = ["""Hey there.
I see you're not feeling so well.
Sometimes life can be rough, but
you will see, things get better."""]


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
            for position in cluster.positions:
                agent = agents.Agent(position[0], position[1], 0, attitude=cluster.attitude)
                self.add_agent(agent)

    def load_agents(self):
        clusters = paulicluster.load_all()
        self.add_clusters(clusters)

    def distance(self, rect1, rect2):
        return math.sqrt((rect1.centerx - rect2.centerx) ** 2 + (rect1.centery - rect2.centery) ** 2)

    def start(self):

        self.camera.bar.set_text(\
        """Hello """ + player_name + """!
        Welcome to the world of cubes. This world is filled with loneliness.
        A lot of cubes feel lonely and you are no exception. How do you overcome this?
        You can move around by using the arrow keys.

        Good luck!""")

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
                    agent.on_enter_personal_space()

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


class Camera:

    def __init__(self, width, height, world, screen=None, top=0, left=0):
        self.height = height
        self.width = width
        self.world = world
        self.max_height = world.end
        self.position = Rect(left, top, width, height)
        self.screen = screen
        self.bar = gui.NarratorBar(Rect(0, 350, self.width, 350))
        self.nametag = gui.TextArea(Rect(50,50,50,20), centered=True)
        self.event_num = 0

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

        if self.event_num < len(event_positions):
            if event_positions[self.event_num] >= self.position.top >= event_positions[self.event_num] - 5:
                self.bar.set_text(event_text[self.event_num])
                self.bar.pop_up()
                self.event_num += 1

    def adjust_agent(self, agent):
        return self.adjust_rect(agent.rect)

    def adjust_rect(self, rect):
        new_left = rect.left - self.position.left
        new_top = rect.top - self.position.top
        return Rect(new_left, new_top, rect.width, rect.height)

    def check_visibility(self, rect):
        return self.position.contains(rect)

    def draw(self):
        self.world.background.draw(self.screen, self.position)

        for agent in self.world.agents:
            if self.check_visibility(agent.rect):
                new_rect = self.adjust_agent(agent)
                self.screen.blit(agent.s, new_rect.topleft)
            else:
                if agent.rect.top > self.position.bottom:
                    self.world.agents.remove(agent)

        self.draw_nametag()
        self.draw_overlay()
        self.bar.draw(self.screen)

    def draw_nametag(self):
        name_area = main_game.player.name_area
        new_rect = self.adjust_rect(name_area)
        self.nametag.move_ip(new_rect.centerx - self.nametag.centerx, new_rect.centery - self.nametag.centery)
        #self.nametag.draw(self.screen)

    def draw_overlay(self, alpha=20):

        s = pygame.Surface((640, 480))  # the size of your rect
        s.set_alpha(alpha)  # alpha level
        s.fill((0, 0, 0))  # this fills the entire surface
        self.screen.blit(s, (0, 0))  # (0,0) are the top-left coordinates
