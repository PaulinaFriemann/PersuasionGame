import sys
import cluster
import pygame

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

        self.clusters = []
        self.end = end_height
        self.background = gui.Background("resources/snowmarc.jpg", [0, 0], screen.get_width(), screen.get_height())
        self.camera = Camera(screen.get_width(), screen.get_height(), self, screen)
        self.player = None
        self.add_player(agents.Player(screen_width / 2, screen_height / 2, 50))
        self.width = screen.get_width()
        self.screen = screen
        self.in_editor_mode = False
        self.cluster_starts = []
        self.action_queue = utils.ActionQueue()

    def add_player(self, player):
        self.player = player

    def add_clusters(self, clusters):
        for cluster in clusters:
            self.clusters.append(cluster)

    def reset_clusters(self, clusters = []):
        #print "SPEDYYY"
        self.clusters = []
        for cluster in clusters:
            self.clusters.append(cluster)

    def load_agents(self):
        clusters = cluster.load_all()
        #print "FIRST"
        self.add_clusters(clusters)
        #self.calc_starts()

    def load_phase(self, phase):
        #print "loading phase " + str(phase)
        clusters = cluster.load_all('clusters/json/all clusters phase ' + str(phase) + '.txt' )
        #print "FIRSTIE FIRST"
        self.music = pygame.mixer.music.load("resources/" + str(phase) + ".mp3")
        pygame.mixer.music.play(-1)

        self.reset_clusters(clusters)
        #self.calc_starts()

    def calc_starts(self):
        for c in self.clusters:
            lowest_y = -999
            for pos in c.starting_positions:
                y = pos[1]
                if y > lowest_y:
                    lowest_y = y
            self.cluster_starts.append(lowest_y)

    def start(self):

        #self.load_agents()
        self.load_phase(1)

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
                if event.type == pygame.KEYUP and event.key == pygame.K_t:
                    self.player.rect.centery = int(raw_input("Teleport to where? "))
                    #self.player.rect.centery = -3500

                if event.type == pygame.KEYUP and event.key == pygame.K_k:
                    print "YOU MONSTER"
                    self.player.happiness = 0

                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    self.player.happy_dance()

            if not self.in_editor_mode:
                self.player.speed = [int(pressed[pygame.K_RIGHT]) - int(pressed[pygame.K_LEFT]),
                                int(pressed[pygame.K_DOWN]) - int(pressed[pygame.K_UP])]

                self.update()

            else:
                self.editor_mode()

            pygame.display.flip()

    def editor_mode(self):
        big_circle = False
        circle = False
        line = False
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
                try:
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_c:
                            n_agents = int(raw_input('How many agents? '))
                            n_space = int(raw_input('How much space do they need? '))
                            if raw_input('Big circle \'b\', or evenly distributed ? ') == "b":
                                big_circle = True
                            else:
                                circle = True

                            print ("A big circle with " if big_circle else "") + str(n_agents) + " agents, " + ("circles worth of agent s" if circle else "") + " and " + str(n_space) + " space between them, got it!"
                            print "Just click to place (:"


                        if event.key == pygame.K_l:
                            n_angle = int(raw_input('What angle? '))
                            n_space = int(raw_input('What space? '))
                            n_agents = int(raw_input('How many agents? '))
                            print "I'll make a line of " + str(n_agents) + " agents, at an angle of " + str(n_angle) + " with " + str(n_space) + " pixels between them."
                            print "Just click to place (:"
                            line = True
                except ValueError:
                    print "That's not a good value."

                if event.type == pygame.QUIT \
                        or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    if len(agent_pos):
                        num_clusters += 1

                        #

                        new_cluster = cluster.Cluster(attitude=attitude,
                                                               starting_positions=[list(pos.center) for pos in agent_pos])
                        cluster.append_to_end(new_cluster)



                if event.type == pygame.KEYUP and event.key == pygame.K_BACKSPACE:
                    if len(agent_pos):
                        num_clusters += 1

                        new_cluster = cluster.Cluster(attitude=attitude,
                                                                starting_positions=[list(pos.center) for pos in agent_pos])
                        self.clusters.append(new_cluster)

                        cluster.append_to_end(new_cluster)
                        new_cluster.add_cluster()
                    self.in_editor_mode = False

            if mousepressed:

                mouse_position = list(pygame.mouse.get_pos())
                mouse_position[1] += self.camera.position.top

                if circle:
                    positions = cluster.evenly_distributed((mouse_position[0], mouse_position[1]), n_space, n_agents)
                    circle = False
                elif big_circle:
                    positions = cluster.big_circle((mouse_position[0],mouse_position[1]),n_space,n_agents)
                    big_circle = False
                elif line:
                    positions = cluster.line((mouse_position[0],mouse_position[1]), n_space, n_angle, n_agents)
                    line = False
                else:
                    positions = [mouse_position]

                for position in positions:
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
        if self.camera.position.top == -4100:
            self.load_phase(3)
        elif self.camera.position.top == -2700:
            self.load_phase(2)

        self.action_queue.step()

        self.update_agents()
        self.update_agents_color()

        self.camera.move(self.player.rect.centery)

        self.camera.draw()
        self.camera.bar.draw(self.screen)
        pygame.display.flip()

    def update_agents(self):
        self.player.update()

        for cluster in self.clusters:
            if self.camera.position.top <= cluster.start_position:
                cluster.update(self.player)
            if not cluster.members:
                self.clusters.remove(cluster)

    def update_agents_color(self):
        for cluster in self.clusters:
            for agent in cluster.members:
                agent.update_color(self.player.happiness)
        self.player.update_color(self.player.happiness)

    def check_close(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT \
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
