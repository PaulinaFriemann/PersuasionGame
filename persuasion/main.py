import sys, pygame
from game import *
from agents import *
from cluster import *
pygame.init()


def main():
    pygame.key.set_repeat(True)

    size = width, height = 640, 480
    white = pygame.Color('White')
    pink = pygame.Color('Pink')
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    agent = Agent(width / 2, height / 2 - 100, pink, screen, movement=movements.random_to_goal)
    player = Player(width/2, height/2, white, screen)

    avoid = Agent(300, 200, pink, screen,movement=movements.circle, attitude=Attitude.avoiding, player=player)

    happy = Agent(380, 280, pink, screen, attitude=Attitude.friendly, player=player)

    #starting screen

    game = Game([happy], screen, 600)
    game.add_player(player)

    rainbow_unicorn_cluster = Cluster(11)
    rainbow_unicorn_cluster.create_cluster((width / 2, height / 2 - 200, 40), 10, avoid, game, Shape.circle)
    rainbow_unicorn_cluster.export_cluster('rainbowcluster.txt')
#    game.start_screen()

    clock = pygame.time.Clock()

    while True:
        clock.tick(30)

        pressed = pygame.key.get_pressed()
        mousepressed = pygame.mouse.get_pressed()

        player.speed[0] = int(pressed[pygame.K_RIGHT]) - int(pressed[pygame.K_LEFT])
        player.speed[1] = int(pressed[pygame.K_DOWN]) - int(pressed[pygame.K_UP])

        if mousepressed[0]:
            print "I'm so happyyy"
            game.add_agent(Agent(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], pink, screen, attitude=Attitude.friendly, player=player))

        if pressed[pygame.K_SPACE]:
            player.colorup(0, 5)

        if pressed[pygame.K_r]:
            rainbow_unicorn_cluster.regroup()

        if pressed[pygame.K_t]:
            rainbow_unicorn_cluster.regroup_wait()

        for event in pygame.event.get():
            if event.type == pygame.QUIT \
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        game.update()


if __name__ == '__main__':
    main()
