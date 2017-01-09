import pygame
import sys

import utils
from pygame import Rect, freetype
import game


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location, camera_width, camera_height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.camera_width = camera_width
        self.camera_height = camera_height
        self.area_horizontal = self.rect.width / 2 - self.camera_width / 2

    def draw(self, screen, camera_position):
        blit_position = Rect(-camera_position.left, 0, camera_position.width, camera_position.height)

        area_vertical   = (self.rect.height - self.camera_height + camera_position.top) % (-self.rect.height)

        screen.blit(self.image, blit_position,
                         area=Rect(self.area_horizontal, area_vertical, self.camera_width, self.camera_height))

        if area_vertical < 0:
            blit_position.height = -area_vertical
            new_area_vertical = self.rect.height + area_vertical
            screen.blit(self.image, blit_position,
                             area=Rect(self.area_horizontal, new_area_vertical, self.camera_width, -area_vertical))


class TextArea(Rect):

    def __init__(self, rect, text="", fontsize=15,
                 fgcolor=pygame.Color("Black"), bgcolor=pygame.Color("White"), alpha=40, centered=True):
        super(TextArea, self).__init__(rect)
        self.text = [text]
        self.font = freetype.SysFont(freetype.get_default_font(), fontsize)
        self.text_color = fgcolor
        self.centered = centered
        self.fontsize = fontsize

        self.s = pygame.Surface((self.width, self.height))  # the size of your rect
        self.s.set_alpha(alpha)  # alpha level
        self.s.fill(bgcolor)  # this fills the entire surface

    def set_text(self, text):
        self.text = text.split("\n")
        self.check_width()

    def check_width(self):
        for line in self.text:
            width = self.font.get_rect(line).width
            if width > self.width:
                self.width = width

    def render(self, screen, absolute=True):
        text_left = self.left + 2
        text_top = self.top + (self.height / 2 - self.fontsize / 2)

        for i, line in enumerate(self.text):
            if not self.centered:
                self.font.render_to(screen, (text_left, text_top + self.font.size * i + 2), line, fgcolor=self.text_color)
            else:
                rect = utils.center_h(self.font.get_rect(line), self)
                if absolute:
                    rect.move_ip([0, self.top])
                self.font.render_to(screen, (rect.center[0], rect.center[1] + self.font.size * i +0),line, fgcolor=self.text_color)

    def draw(self, screen):
        screen.blit(self.s, self.topleft)
        self.render(screen)


class Button(TextArea):

    def __init__(self, rect, text="", fgcolor=(255,255,255),bgcolor=(50,50,50)):
        super(Button, self).__init__(rect, text=text, fgcolor=fgcolor, bgcolor=bgcolor)


class TextField(TextArea):

    def __init__(self, rect, text="", fgcolor=(255,255,255),bgcolor=(50,50,50)):
        super(TextField, self).__init__(rect, text=text, fgcolor=fgcolor, bgcolor=bgcolor, centered=False)

    def add_letter(self, letter):
        _, rect = self.font.render(self.text[-1] + letter)
        if rect.width < self.width - 2:
            self.text[-1] += letter

    def delete_letter(self):
        self.text[-1] = self.text[-1][:-1]


class StartScreen:

    def __init__(self, screen):

        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.background = Background("resources/bankbig.jpg", [0, 0], self.width, self.height)

        self.start_button = TextArea(Rect(270, 342, 100, 30), fgcolor=(255,255,255),bgcolor=(50,50,50))
        print self.start_button
        self.start_button.set_text("Start Game")
        self.start_text = TextArea(Rect(screen.get_width() / 2 - 400/ 2, 100, 400, 100))

        self.start_text.set_text(
            """Please enter your name""")

        self.player_name = TextField(utils.center_rect(Rect(0, 0, 200, 30), self.screen.get_rect()))

    def start(self):
        name_entered = False
        while not name_entered:

            pressed = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT \
                        or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos, button = event.pos, event.button
                    if self.start_button.collidepoint(*pos):
                        name_entered = True
                if event.type == pygame.KEYUP:
                    if pygame.K_a <= event.key <= pygame.K_z:
                        if not pressed[pygame.K_LSHIFT] and not pressed[pygame.K_RSHIFT]:
                            self.player_name.add_letter(pygame.key.name(event.key))
                        else:
                            self.player_name.add_letter(pygame.key.name(event.key).upper())
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name.delete_letter()
                    elif event.key == pygame.K_RETURN:
                        name_entered = True

            self.background.draw(self.screen, self.screen.get_rect())
            self.start_text.draw(self.screen)
            self.start_button.draw(self.screen)
            self.player_name.draw(self.screen)
            pygame.display.flip()

        return self.player_name.text[0]


class NarratorBar(TextArea):

    def __init__(self, rect):

        super(NarratorBar, self).__init__(rect, centered=True, fgcolor=pygame.Color("White"), fontsize=16)
        self.visibility_status = 0
        self.popup = False
        self.max_top = rect.top
        self.top = game.screen_height

    def set_text(self, text):
        super(NarratorBar, self).set_text(text)

    def pop_up(self):
        self.popup = True
        #print self.visibility_status

    def get_visible(self, screen_height):
        if self.popup and self.visibility_status < 150:
            self.visibility_status += 2
            self.move_ip(0,-2)
        elif self.popup and 150 <= self.visibility_status  < 800:
            self.visibility_status += 2

        elif self.popup and self.visibility_status >= 800:
            self.popup = False
        elif not self.popup and self.visibility_status > 650:
            self.visibility_status -= 2
            self.move_ip(0,2)
        elif not self.popup and self.visibility_status <= 650:
            self.visibility_status = 0

    def draw(self, screen):
        if self.popup or self.visibility_status != 0:
            self.get_visible(screen.get_height())
            self.render(screen, True)
