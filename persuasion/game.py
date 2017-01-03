import pygame
from pygame import Rect
import agents
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
        self.agents.append(agent)

    def add_player(self, player):
        self.agents.append(player)
        self.player = player

    def distance(self, rect1, rect2):
        return math.sqrt((rect1.centerx - rect2.centerx) ** 2 + (rect1.centery - rect2.centery) ** 2)

    def start(self):
        self.start_screen()
        print self.camera.bar.text
        self.camera.bar.set_text(\
        """Hello """ + self.player_name.text[0] + """!
        Welcome to the world of cubes. This world is filled with loneliness.
        A lot of cubes feel lonely and you are no exception. How do you overcome this?
        You can move around by using the arrow keys.

        Good luck!""")

    def update(self):

        self.check_close()

        self.action_queue.step()

        self.update_agents()

        self.camera.move(self.player.speed)

        self.camera.draw()
        self.camera.bar.draw(self.screen)
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

        background = gui.Background("resources/street.jpg", [0, 0], self.screen.get_width(), self.screen.get_height())

        start_button = gui.Button(270, 342, 100, 30)
        start_button.set_text("Start Game")

        start_text = gui.TextArea(15, Rect(self.width/2 - 200,40,400,100), centered=True)

        start_text.set_text(
        """Welcome
        Please enter your name""")

        self.player_name = gui.TextArea(15, utils.center_rect(Rect(0,0,200,30), self.screen.get_rect()))
        self.player_name.set_changeable(True)
        name_entered = False
        while not name_entered:

            pressed = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT \
                        or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos, button = event.pos, event.button
                    if start_button.collidepoint(*pos):
                        name_entered = True
                if event.type == pygame.KEYUP:
                    if pygame.K_a <= event.key <= pygame.K_z:
                        if not pressed[pygame.K_LSHIFT] and not pressed[pygame.K_RSHIFT]:
                            self.player_name.add_letter(pygame.key.name(event.key))
                        else:
                            self.player_name.add_letter(pygame.key.name(event.key).upper())
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name.delete_letter()
                    elif event.key == pygame.K_RETURN:
                        name_entered = True


            background.draw(self.screen, self.camera.position)
            start_text.draw(self.screen)
            #self.screen.fill([0,0,0])
            start_button.draw(self.screen)
            self.player_name.draw(self.screen)
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
