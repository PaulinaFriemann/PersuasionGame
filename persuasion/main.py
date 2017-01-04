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




def main():


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

    rainbow_unicorn_cluster = Cluster(11)
    rainbow_unicorn_cluster.evenly_distributed((200, 0), avoid.width * 2, 10, avoid, settings.game)

    rainbow_unicorn_cluster = Cluster(3)
    rainbow_unicorn_cluster.evenly_distributed((400, 0), happy.width * 2, 4, happy, settings.game)


    clock = pygame.time.Clock()
    settings.game.camera.bar.pop_up()

    mouse_is_pressed = False

  #  agentlist = [
   #     cluster_avoid, cluster_avoid, cluster_happy,
   # ]

#    initialize_clusters(agentlist, settings.game)

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
