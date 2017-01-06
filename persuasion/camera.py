import pygame
from pygame import Rect
import gui
import game


event_positions = [-500, -1000]
event_text = ["""Hey there.
I see you're not feeling so well.
Sometimes life can be rough, but
you will see, things get better.""", """When you hit rock bottom,
there is only one way to go."""]


class Camera:

    def __init__(self, width, height, world, screen=None, top=0, left=0):
        self.height = height
        self.width = width
        self.world = world
        self.max_height = world.end
        self.position = Rect(left, top, width, height)
        self.screen = screen
        self.bar = gui.NarratorBar(Rect(0, 350, self.width, 350))
        self.event_num = 0

        self.bar.set_text("""Hello """ + game.player_name + """!
        Welcome to the world of cubes.
        This world is filled with loneliness.
        A lot of cubes feel lonely and you are no exception.
        How do you overcome this?
        You can move around by using the arrow keys.""")

    def move(self, player_center):

        self.position.centery = player_center[1]

        if self.event_num < len(event_positions):
            if event_positions[self.event_num] >= self.position.top >= event_positions[self.event_num] - 5:
                self.bar.set_text(event_text[self.event_num])
                #self.bar.pop_up()
                self.event_num += 1

    def adjust_agent(self, agent):
        return self.adjust_rect(agent.rect)

    def adjust_rect(self, rect):
        new_left = rect.left - self.position.left
        new_top = rect.top - self.position.top
        return Rect(new_left, new_top, rect.width, rect.height)

    def check_visibility(self, rect):
        return self.position.contains(rect)

    def draw(self):
        self.world.background.draw(self.screen, self.position)
        for cluster in self.world.clusters:
            if self.position.top <= cluster.start_position:
                for agent in cluster.members:
                    if self.check_visibility(agent.rect):
                        new_rect = self.adjust_agent(agent)
                        self.screen.blit(agent.s, new_rect.topleft)
                    else:
                        if agent.rect.top > self.position.bottom:
                            cluster.members.remove(agent)
        new_rect = self.adjust_agent(self.world.player)
        self.screen.blit(self.world.player.s, new_rect.topleft)

        self.draw_overlay(100 - self.world.player.happiness)
        self.bar.draw(self.screen)

    def draw_overlay(self, alpha=0):

        s = pygame.Surface((640, 480))  # the size of your rect
        s.set_alpha(alpha)  # alpha level
        s.fill((0, 0, 0))  # this fills the entire surface
        self.screen.blit(s, (0, 0))  # (0,0) are the top-left coordinates