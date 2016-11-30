import sys, pygame
from game import *
pygame.init()


class Agent:

    def __init__(self, x, y, color, screen):
        self.x = x
        self.y = y
        self.color = color
        self.width = 6
        self.height = 6
        self.speed = [0,0]
        self.screen = screen

    def get_rect(self):
        return pygame.Rect(self.x - self.width / 2,
                           self.y - self.height / 2,
                           self.width, self.height)

    def set_rect(self, rect):
        self.x = rect.left + self.width/2
        self.y = rect.top + self.height/2

    def move(self, speed):
        speed = map(lambda x: 2*x, speed)
        new_x = self.get_rect().bottomright[0] + speed[0]
        if self.screen.get_width() > new_x > (0 + self.width):
            self.set_rect(self.get_rect().move(speed))

    def update(self):
        self.move(self.speed)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.get_rect())


def main():

    pygame.key.set_repeat(True)

    size = width, height = 320, 240
    black = 0, 0, 0
    white = pygame.Color(255, 255, 255, 255)

    screen = pygame.display.set_mode(size)
    camera = Camera(complex_camera, width, height * 2)

    #agents = [Agent(width/2, height - 20, white)]
    player = Agent(width/2, height - 20, white, screen)

    clock = pygame.time.Clock()

    while 1:

        clock.tick(30)

        pressed = pygame.key.get_pressed()

        camera.update(player)

        player.speed[1] = int(pressed[pygame.K_DOWN]) - int(pressed[pygame.K_UP])
        player.speed[0] = int(pressed[pygame.K_RIGHT]) - int(pressed[pygame.K_LEFT])

        for event in pygame.event.get():
            if event.type == pygame.QUIT \
            or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    sys.exit()

        player.update()

        screen.fill(black)
        pygame.draw.rect(screen, player.color, camera.apply(player))
        #player.draw()
        pygame.display.flip()


if __name__ == '__main__':
    main()