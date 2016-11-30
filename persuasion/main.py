import sys, pygame
pygame.init()


class Agent:

    def __init__(self, x, y, color, player = False):
        self.player = player 
        self.x = x
        self.y = y
        self.color = color
        self.width = 6
        self.height = 6
        self.image = pygame.Surface((self.width,self.height))
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

    size = width, height = 640, 480
    black = 0, 0, 0
    white = pygame.Color('White')
    pink = pygame.Color('Pink')

    screen = pygame.display.set_mode(size)
    world = pygame.Surface((1000,1000))

    agent = Agent(width/2, height/2 - 100, pink)
    player = Agent(500, 500, white, True)

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
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.update()
        agent.update()

        screen.fill(black)
        world.fill(black)
        
        pygame.draw.rect(world, player.color, player.get_rect())
        pygame.draw.rect(world, agent.color, agent.get_rect())

        world.blit(player.image,(player.x,player.y))
        screen.blit(world,(player.speed[0]*6,player.speed[1]*6))
        
        pygame.display.flip()


if __name__ == '__main__':
    main()
