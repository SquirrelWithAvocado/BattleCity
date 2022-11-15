import pygame

from UI.cursor import Cursor
from UI.hole import Hole


class MouseHandler:
    def __init__(self, buttons, surface):
        self.buttons = buttons

        self.surface = surface
        self.holes_limit = 10
        self.holes = []
        self.cursor = Cursor(self.surface)

    def mouse_event(self, type, coords):
        for button in self.buttons:
            if type == pygame.MOUSEMOTION:
                self.mouse_move(coords, button)
            elif type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down(coords, button)
            elif type == pygame.MOUSEBUTTONUP:
                self.mouse_up(coords, button)

        for hole in self.holes:
            hole.draw()

        self.cursor.update(coords)

    def mouse_move(self, coords, button):
        if button.rect.collidepoint(coords):
            button.color = 'light gray'
        else:
            button.color = 'white'

    def mouse_down(self, coords, button):
        if button.rect.collidepoint(coords):
            button.color = 'gray'

        if len(self.holes) == self.holes_limit:
            self.holes.pop(0)
        self.holes.append(Hole(coords, self.surface))

    def mouse_up(self, coords, button):
        if button.rect.collidepoint(coords):
            button.on_click(self)
            button.color = 'light gray'
