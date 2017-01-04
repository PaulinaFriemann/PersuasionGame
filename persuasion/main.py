from agents import *
from cluster import *
import settings
import sys
import utils
import paulicluster

pygame.init()


def init():
    pygame.key.set_repeat(True)
    settings.init(500, 480)


def main():
    init()

    agent_pos = []

    clusters = paulicluster.load_all()

    print clusters

    player_pos = pygame.Rect(settings.screen_width / 2 - 5, settings.screen_height / 2 - 5, 10, 10)
    clock = pygame.time.Clock()
    block = 0
    num_clusters = 0
    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT \
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                if len(agent_pos):
                    num_clusters += 1
                    cluster = paulicluster.PauliCluster(number=num_clusters, attitude=Attitude.avoiding.value, positions=[list(pos.center) for pos in agent_pos])

                    paulicluster.move_cluster(cluster, 0, 200)

                    paulicluster.append_to_end(cluster)

                pygame.quit()
                sys.exit()

        mousepressed = pygame.mouse.get_pressed()[0] if block == 0 else False

        if mousepressed:

            position = pygame.mouse.get_pos()
            rect = utils.get_rect(position[0], position[1], 10, 10)
            if any([rect.colliderect(other) for other in agent_pos]):
                colliders = filter(rect.colliderect, agent_pos)
                for col in colliders:
                    agent_pos.remove(col)
            else:
                agent_pos.append(rect)
            block = 10

        block = max(0, block -1)

        #print agent_pos

        settings.game.screen.fill([250, 250, 205])
        pygame.draw.rect(settings.game.screen, pygame.Color("Black"), player_pos)

        for cluster in clusters:
            for pos in cluster.positions:
                pygame.draw.rect(settings.game.screen, pygame.Color("Blue"), utils.get_rect(pos[0], pos[1], 10, 10))

        for pos in agent_pos:
            pygame.draw.rect(settings.game.screen, pygame.Color("Black"), pos)

        pygame.display.flip()


def mainb():

    init()

    white = pygame.Color('White')
    pink = pygame.Color('Pink')
    black = 0, 0, 0


    #agent = Agent(width / 2, height / 2 - 100, pink, screen, movement=movements.random_to_goal)
    player = Player(settings.screen_width/2, settings.screen_height/2, 0)

    avoid = Agent(300, 200, 0, movement=movements.circle, attitude=Attitude.avoiding, cluster_member=True)
    neutral = Agent(300, 200, 50, movement=movements.circle, attitude=Attitude.avoiding, cluster_member=True)
    happy = Agent(380, 280, 100, attitude=Attitude.friendly)

    settings.game.add_agent(happy)
    settings.game.add_agent(neutral)
    settings.game.add_player(player)

    settings.game.start()

    cluster_happy = Dummy(pink, attitude=Attitude.friendly)
    cluster_avoid = Dummy(white, attitude=Attitude.avoiding)

    rainbow_unicorn_cluster = Cluster(11)
    rainbow_unicorn_cluster.evenly_distributed((200, 0), avoid.width * 2, 10, avoid, settings.game)

    rainbow_unicorn_cluster = Cluster(3)
    rainbow_unicorn_cluster.evenly_distributed((400, 0), happy.width * 2, 4, happy, settings.game)


    clock = pygame.time.Clock()
    settings.game.camera.bar.pop_up()

    mouse_is_pressed = False

    agentlist = [
        cluster_avoid, cluster_avoid, cluster_happy,
    ]

    initialize_clusters(agentlist, settings.game)

    while True:
        clock.tick(30)

        pressed = pygame.key.get_pressed()
        mousepressed = pygame.mouse.get_pressed()

        player.speed[0] = int(pressed[pygame.K_RIGHT]) - int(pressed[pygame.K_LEFT])
        player.speed[1] = int(pressed[pygame.K_DOWN]) - int(pressed[pygame.K_UP])

        if mousepressed[0]:
            mouse_is_pressed = True

        if not mousepressed[0] and mouse_is_pressed:
            print pygame.mouse.get_pos()
            mouse_is_pressed = False

        if pressed[pygame.K_SPACE]:
            player.colorup(0, 5)

        if pressed[pygame.K_r]:
            rainbow_unicorn_cluster.regroup()

        if pressed[pygame.K_t]:
            rainbow_unicorn_cluster.regroup_wait()

        settings.game.update()


if __name__ == '__main__':
    main()
