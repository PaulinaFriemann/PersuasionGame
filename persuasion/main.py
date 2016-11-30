import sys, pygame
pygame.init()


class Agent:

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = 6
        self.height = 6
        self.speed = [0,0]
        

    def get_rect(self):
        return pygame.Rect(self.x - self.width / 2,
                           self.y - self.height / 2,
                           self.width, self.height)

    def set_rect(self, rect):
        self.x = rect.left + self.width/2
        self.y = rect.top + self.height/2

    def move(self, speed):
        self.set_rect(self.get_rect().move(speed))

    def colorup(self, dh = 0,ds = 0,dv = 0):
        h,s,v,a = self.color.hsva
        if(h + dh <= 255 and s + ds <= 100 and v + dv <= 100):
            self.color.hsva = (h+dh,s+ds,v+dv,a)

    def update(self):
        self.move(self.speed)

def main():

    pygame.key.set_repeat(True)

    size = width, height = 320, 240
    black = 0, 0, 0
    white = pygame.Color('White')

    screen = pygame.display.set_mode(size)

    #agents = [Agent(width/2, height - 20, white)]
    player = Agent(width/2, height - 20, white)

    player.color.hsva = (180,0,50,100)
    
    clock = pygame.time.Clock()

    while 1:

        clock.tick(30)

        pressed = pygame.key.get_pressed()

        player.speed[1] = int(pressed[pygame.K_DOWN]) - int(pressed[pygame.K_UP])
        player.speed[0] = int(pressed[pygame.K_RIGHT]) - int(pressed[pygame.K_LEFT])

        if pressed[pygame.K_SPACE]:
            player.colorup(0,10)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        player.update()

        screen.fill(black)
        pygame.draw.rect(screen, player.color, player.get_rect())
        pygame.display.flip()


if __name__ == '__main__':
    main()
