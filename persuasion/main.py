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
        return pygame.Rect(self.x - self.width/2,
                           self.y - self.height/2,
                           self.width, self.height)

    def set_rect(self, rect):
        self.x = rect.left + self.width/2
        self.y = rect.top + self.height/2


size = width, height = 320, 240
speed = [0,2]
black = 0, 0, 0
white = pygame.Color(255, 255, 255, 255)

screen = pygame.display.set_mode(size)

agents = [Agent(width/2, height - 20, white)]

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        agents[0].set_rect( agents[0].get_rect().move(speed))
        if agents[0].get_rect().left < 0 or agents[0].get_rect().right > width:
            speed[0] = -speed[0]

        if agents[0].get_rect().top < 0 or agents[0].get_rect().bottom > height:
            speed[1] = -speed[1]

        screen.fill(black)
        pygame.draw.rect(screen, agents[0].color, agents[0].get_rect())
        pygame.display.flip()