from agents import *
#from cluster import *
import settings
import sys
import utils
import cluster
import game
from simple_model import Attribute

pygame.init()


def init():
    pygame.key.set_repeat(True)
    game.init(500, 480)


def mainfds():

    clusters = cluster.load_all()

    cluster.save_all(clusters)


def main():
    init()


def maiasdn():

    init()

    clusters = cluster.load_all()

    #cluster.move_cluster(clusters[-3], 0, -100)
    #cluster.move_cluster(clusters[-2], 0, -100)
    #cluster.move_cluster(clusters[-1], 0, -100)

    cluster.save_all(clusters)


def mainsad():
    init()

    white = pygame.Color('White')
    pink = pygame.Color('Pink')
    black = 0, 0, 0

    player = Player(game.screen_width/2, game.screen_height/2, 100)
    game.main_game.add_player(player)

    game.main_game.start()

    clusters = cluster.load_all()
    for cluster in clusters:

        cluster.add_cluster(game = game.main_game)

    #settings.game.add_clusters(clusters)

    clock = pygame.time.Clock()
    game.main_game.camera.bar.pop_up()

    mouse_is_pressed = False

    while True:
        clock.tick(30)

        pressed = pygame.key.get_pressed()
        mousepressed = pygame.mouse.get_pressed()

        player.speed[0] = int(pressed[pygame.K_RIGHT]) - int(pressed[pygame.K_LEFT])
        player.speed[1] = int(pressed[pygame.K_DOWN]) - int(pressed[pygame.K_UP])
        #player.speed[1] = - int(pressed[pygame.K_UP])

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

        game.main_game.update()


def mainasd():
    init()

    agent_pos = []

    clusters = cluster.load_all()

    cluster.move_cluster(clusters[1], 0, -200)
    cluster.move_cluster(clusters[2], 0, -200)

    print clusters

    player_pos = pygame.Rect(game.screen_width / 2 - 5, game.screen_height / 2 - 5, 10, 10)
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

                    try:
                        cluster = cluster.Cluster(number=num_clusters, attitude=Attitude.avoiding.value, positions=[list(pos.center) for pos in agent_pos])
                    except AttributeError:
                        cluster = cluster.Cluster(number=num_clusters, attitude=Attitude.avoiding, positions=[list(pos.center) for pos in agent_pos])

                    cluster.append_to_end(cluster)

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

        game.screen.fill([250, 250, 205])
        pygame.draw.rect(game.main_game.screen, pygame.Color("Black"), player_pos)

        #for cluster in clusters:
         #   for pos in cluster.positions:
                #pygame.draw.rect(settings.game.screen, pygame.Color("Blue"), utils.get_rect(pos[0], pos[1], 10, 10))

        for pos in agent_pos:
            pygame.draw.rect(game.main_game.screen, pygame.Color("Black"), pos)

        pygame.display.flip()



if __name__ == '__main__':
    main()
