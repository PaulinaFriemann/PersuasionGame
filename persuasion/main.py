import sys, pygame
from game import *
from agents import *
pygame.init()


def main():
    pygame.key.set_repeat(True)

    size = width, height = 640, 480
    white = pygame.Color('White')
    pink = pygame.Color('Pink')
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    agent = Agent(width / 2, height / 2 - 100, pink, screen, movement=movements.move_path)
    player = Player(width/2, height/2, white, screen)

    avoid = Agent(200, 300, pink, screen,movement=movements.move_path, behavior=behaviors.avoid, player=player)

    happy = Agent(380, 280, pink, screen, behavior=behaviors.make_happy, player=player)

    game = Game([agent, avoid, happy], screen, 600)
    game.add_player(player)

    clock = pygame.time.Clock()

    while True:
        clock.tick(30)

        pressed = pygame.key.get_pressed()

        player.speed[0] = int(pressed[pygame.K_RIGHT]) - int(pressed[pygame.K_LEFT])
        player.speed[1] = int(pressed[pygame.K_DOWN]) - int(pressed[pygame.K_UP])

        if pressed[pygame.K_SPACE]:
            player.colorup(0, 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT \
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        game.update()


if __name__ == '__main__':
    main()
