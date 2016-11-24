import sys, pygame
pygame.init()


class Agent:

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = 5
        self.height = 5

    def get_rect(self):
        return pygame.Rect(self.x - self.width / 2,
                           self.y - self.height / 2,
                           self.width, self.height)

    def set_rect(self, rect):
        self.x = rect.left + self.width/2
        self.y = rect.top + self.height/2

    def move(self, speed):
        self.set_rect(self.get_rect().move(speed))


class Player(Agent):

    def __init__(self, x, y, color, screen):
        Agent.__init__(self, x, y, color)
        self.speed = [0, 0]
        self.screen = screen

    def moveup(self):
        self.speed = [0, -1]

    def stop(self):
        self.speed = [0, 0]

    def update(self):
        self.move(self.speed)
        pygame.event.pump()


def main():

    pygame.key.set_repeat(True)

    size = width, height = 320, 240
    black = 0, 0, 0
    white = pygame.Color(255, 255, 255, 255)

    screen = pygame.display.set_mode(size)

    agents = [Agent(width/2, height - 20, white)]
    player = Player(width/2, height - 20, white, screen)

    clock = pygame.time.Clock()

    while 1:

        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.moveup()

            #elif event.type == pygame.KEYUP:
             #   if event.key == pygame.K_UP:
              #      player.stop()

            player.update()

            screen.fill(black)

            pygame.draw.rect(screen, player.color, player.get_rect())
            pygame.display.flip()


if __name__ == '__main__':
    main()