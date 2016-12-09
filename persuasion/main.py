import sys, pygame
from game import *
pygame.init()


def main():
    pygame.key.set_repeat(True)

    size = width, height = 640, 480
    white = pygame.Color('White')
    pink = pygame.Color('Pink')
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    agent = Agent(width / 2, height / 2 - 100, pink, screen)
    player = Player(width/2, height/2, white, screen)

    game = Game([agent], screen, 600)
    game.add_player(player)

    #player.color.hsva = (50, 20, 50, 100)

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
