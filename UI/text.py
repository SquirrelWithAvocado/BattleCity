import pygame
from pygame.locals import *


class Text:
    """Text object creation."""

    def __init__(self, text, pos, fontsize=16, color='black'):
        self.text = text
        self.pos = pos

        self.fontname = None
        self.fontsize = fontsize
        self.fontcolor = Color(color)
        self.set_font()
        self.render()

    def set_font(self):
        """Font setting."""
        self.font = pygame.font.Font(self.fontname, self.fontsize)

    def render(self):
        """Render text to image"""
        self.image = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def draw(self, screen):
        """Draw image"""
        screen.blit(self.image, self.rect)
