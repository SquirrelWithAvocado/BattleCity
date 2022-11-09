import pygame
from UI.text import Text


class Button:
    def __init__(self, coords, scale, text, on_click=lambda x: None):
        self.color = 'white'
        self.on_click = on_click

        x, y = coords[0], coords[1]
        w, h = scale[0], scale[1]

        self.rect = pygame.Rect((x, y, w, h))
        self.text = Text(text, self.rect.center, fontsize=32)

    def draw(self, surface):
        pygame.draw.rect(surface, pygame.Color(self.color), self.rect)
        self.text.draw(surface)
