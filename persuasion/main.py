from agents import *
from cluster import *
import settings
import __builtin__
import random
import math

pygame.init()


def init():
    pygame.key.set_repeat(True)
    settings.init(640, 480)


# density will be multiplicated by the space this amount of agents needs. (density * ceil(sqrt(personal_space)))
def initialize_clusters(agentlist, game, n_minagents = 2, n_maxagents = 10,
                        min_personal_space = 9, max_personal_space = 20,
                        min_density = 1.5, max_density = 2,
                        min_space_between_clusters = 3, max_space_between_clusters = 8):

    n_clusters = len(agentlist)
    clusters = []
    clusters_starting_locations = []
    clusters_n_agents = []
    clusters_personal_space = []
    clusters_density = []
    clusters_space_between_clusters = []

    for i in range(n_clusters):
        clusters.append(Cluster(i))
        clusters_n_agents.append(random.randint(n_minagents, n_maxagents))
        clusters_personal_space.append(random.randint(min_personal_space, max_personal_space))
        clusters_density.append(random.uniform(min_density, max_density))
        clusters_space_between_clusters.append(random.uniform(min_space_between_clusters, max_space_between_clusters))

        radius = int(math.ceil(clusters_density[i] * math.sqrt(clusters_n_agents[i])*clusters_personal_space[i]))
        print radius
        if i > 0:
            y = math.ceil(clusters_starting_locations[i - 1][1] - (
            clusters_starting_locations[i - 1][2] * clusters_space_between_clusters[i]))
        else:
            y = 0

        x = random.randint(radius + 4, game.width - (radius + 4))
        clusters_starting_locations.append((x, y, radius))
        with open("clusterinfo " + str(i) + ".txt", 'w') as f:
            f.write(str(clusters_n_agents[i]) +  '\n')
            f.write(str(clusters_personal_space[i]) +  '\n')
            f.write(str(clusters_density[i]) +  '\n')
            f.write(str(clusters_space_between_clusters[i]) +  '\n')
            f.write(str(clusters_starting_locations[i]) +  '\n')

    for i in range(len(clusters)):
        clusters[i].create_cluster(clusters_starting_locations[i], clusters_n_agents[i], agentlist[i], game, Shape.circle)
        clusters[i].to_pickle('Cluster ' + str(i) + '.cluster')


def main():


    init()

    white = pygame.Color('White')
    pink = pygame.Color('Pink')
    black = 0, 0, 0


    #agent = Agent(width / 2, height / 2 - 100, pink, screen, movement=movements.random_to_goal)
    player = Player(settings.screen_width/2, settings.screen_height/2, white)

   # avoid = Agent(300, 200, pink, screen,movement=movements.circle, attitude=Attitude.avoiding, cluster_member=True, player=player)

    happy = Agent(380, 280, pink, attitude=Attitude.friendly)
    settings.game.add_agent(happy)
    settings.game.add_player(player)

  #  rainbow_unicorn_cluster = Cluster(11)
   # rainbow_unicorn_cluster.create_cluster((width / 2, height / 2 - 200, 40), 10, avoid, game, Shape.circle)
    #rainbow_unicorn_cluster.export_cluster('rainbowcluster.txt')

    settings.game.start()

    cluster_happy = Dummy(pink, attitude=Attitude.friendly)
    cluster_avoid = Dummy(white, attitude=Attitude.avoiding)

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
