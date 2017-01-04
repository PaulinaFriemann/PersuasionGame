import pygame
import utils
from pygame import Rect, freetype


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


class Button(Rect):

    def __init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)

    def set_text(self, text):
        self.text = text

        self.font = freetype.SysFont(freetype.get_default_font(), 15)
        self.text_rect = utils.center_rect(self.font.get_rect(text), self)

    def draw(self, screen):
        pygame.draw.rect(screen, [50,50,50], self)
        self.font.render_to(screen, self.text_rect.topleft,
                           self.text, fgcolor = (255,255,255))

    def on_click(self):
        pass


class TextArea(Rect):

    def __init__(self, font_size, rect, centered=False):
        super(TextArea, self).__init__(rect)

        self.font = freetype.SysFont(freetype.get_default_font(), font_size)
        self.text = [""]
        self.text_top = self.top + (self.height/2 - font_size/2)
        self.text_left = self.left + 2
        self.changeable = False
        self.color = pygame.Color(200,200,200)
        self.centered = centered

        self.s = pygame.Surface((self.width, self.height))  # the size of your rect
        self.s.set_alpha(40)  # alpha level
        self.s.fill(self.color)  # this fills the entire surface

    def set_color(self, color):
        self.color = color
        self.s.fill(self.color)

    def set_changeable(self, changeable):
        self.changeable = changeable

    def set_text(self, text):
        self.text = text.split("\n")

    def add_letter(self, letter):
        if self.changeable and len(self.text) == 1:
            _, rect = self.font.render(self.text[-1] + letter)
            if rect.width < self.width - 2:
                self.text[-1] += letter

    def delete_letter(self):
        if self.changeable and len(self.text) == 1:
            self.text[-1] = self.text[-1][:-1]

    def render(self, screen):
        for i, line in enumerate(self.text):
            if not self.centered:
                self.font.render_to(screen, (self.text_left, self.text_top + self.font.size * i + 2), line)
            else:

                rect = utils.center_h(self.font.get_rect(line), self)
                self.font.render_to(screen, (rect.center[0], rect.center[1] + self.font.size * i + 2),line)

    def draw(self, screen):
        screen.blit(self.s, self.topleft)
        self.render(screen)


class NarratorBar(TextArea):

    def __init__(self, font_size, rect):
        super(NarratorBar, self).__init__(font_size, rect)
        self.image = pygame.image.load("resources/bar.jpg")
        self.image.set_alpha(100)
        self.visibility_status = 0
        self.popup = False

    def set_text(self, text):
        super(NarratorBar, self).set_text(text)
        self.image = pygame.image.load("resources/bar.jpg")
        self.image.set_alpha(100)

        for i, line in enumerate(self.text):
            rect = utils.center_horizontal(self.font.get_rect(line), self.width)
            self.font.render_to(self.image, (rect.center[0], rect.center[1] + self.font.size * i + 2), line)

    def pop_up(self):
        self.popup = True

    def get_visible(self):
        if self.popup and self.visibility_status < self.height + 100:
            self.visibility_status += 2
        elif self.popup and self.visibility_status == self.height + 100:
            self.popup = False
        elif not self.popup and self.visibility_status > 0:
            self.visibility_status -= 2

    def draw(self, screen):
        self.get_visible()
        screen.blit(self.image, (0, max(screen.get_height() - self.visibility_status, self.top)))