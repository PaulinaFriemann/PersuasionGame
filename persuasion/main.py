import sys, pygame
pygame.init()
from game import *


def main2():

    pygame.key.set_repeat(True)

    size = width, height = 640, 480
    black = 0, 0, 0
    white = pygame.Color('White')
    pink = pygame.Color('Pink')

    screen = pygame.display.set_mode(size)

#    player = Agent(width/2, height - 20, white, screen)

    world = pygame.Surface((1000,1000))

    agent = Agent(width/2, height/2 - 100, pink, screen)
    player = Agent(500, 500, white, screen, True)

    player.color.hsva = (50,20,50,100)
    
    clock = pygame.time.Clock()

    while 1:

        clock.tick(30)

        pressed = pygame.key.get_pressed()

        player.speed[0] = int(pressed[pygame.K_RIGHT]) - int(pressed[pygame.K_LEFT])
        player.speed[1] = int(pressed[pygame.K_DOWN]) - int(pressed[pygame.K_UP])

        world.scroll(player.speed[0],player.speed[1])
        
        if pressed[pygame.K_SPACE]:
            player.colorup(0,5)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT \
            or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

        player.update()
        agent.update()

        screen.fill(black)

        world.fill(black)
        
        pygame.draw.rect(world, player.color, player.rect)
        pygame.draw.rect(world, agent.color, agent.rect)

        world.blit(player.image,(player.x,player.y))
        screen.blit(world,(player.speed[0]*6,player.speed[1]*6))

        pygame.display.flip()


def main():
    pygame.key.set_repeat(True)

    size = width, height = 640, 480
    white = pygame.Color('White')
    pink = pygame.Color('Pink')
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    agent = Agent(width / 2, height / 2 - 100, pink, screen)
    player = Agent(width/2, 400, white, screen, True)

    world = World([player, agent], width, 600)
    camera = Camera(width, height, world, screen)
    camera.calibrate(player)

    #  player = Agent(width/2, height - 20, white, screen)

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


        player.update()
        agent.update()

        camera.move(player.speed)

        screen.fill([0, 0, 0])
        blit_position = Rect(camera.position.left, -camera.position.top, camera.position.width, camera.position.width)
        screen.blit(world.background.image, blit_position)


        camera.draw()

        pygame.display.flip()


if __name__ == '__main__':
    main()
