import pygame
import utils
from pygame import Rect


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

        self.font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 15)
        self.text_rect = utils.center_rect(self.font.get_rect(text), self)

    def draw(self, screen):
        pygame.draw.rect(screen, [200,200,200], self)
        self.font.render_to(screen, self.text_rect.topleft,
                           self.text, fgcolor = (150,20,255))


class TextArea(Rect):

    def __init__(self, font_size, *args, **kwargs):
        super(TextArea, self).__init__(*args, **kwargs)

        self.font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), font_size)
        self.text = ""
        self.text_top = self.top + (self.height/2 - font_size/2)
        self.text_left = self.left + 2

    def set_text(self, text):
        self.text = text

    def add_letter(self, letter):
        self.text += letter

    def delete_letter(self):
        self.text = self.text[:-1]

    def draw(self, screen):
        pygame.draw.rect(screen, [200,200,200], self)
        self.font.render_to(screen, (self.text_left, self.text_top),
                           self.text, fgcolor = (150,20,255))


class NarratorBar(TextArea):

    def __init__(self, font_size, *args, **kwargs):
        super(NarratorBar, self).__init__(font_size, *args, **kwargs)
        self.image = pygame.image.load("resources/bar.jpg")
        self.image.set_alpha(100)
        self.set_text("Hallo wie gehts?")

    def set_text(self, text):
        self.text = text
        rect = utils.center_horizontal(self.font.get_rect(text), self.width)
        label = self.font.render_to(self.image, rect.center, text)

    def draw(self, screen):

        screen.blit(self.image, (0, 350))  # (0,0) are the top-left coordinates