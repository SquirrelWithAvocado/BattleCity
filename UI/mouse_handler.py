import pygame

from UI.hole import Hole


class MouseHandler:
    def __init__(self, buttons, surface, holes):
        self.buttons = buttons
        self.surface = surface
        self.holes_limit = 10
        self.holes = holes

    def mouse_event(self, event_type, coords):
        if event_type == pygame.MOUSEMOTION:
            self.mouse_move(coords)
        elif event_type == pygame.MOUSEBUTTONDOWN:
            self.mouse_down(coords)
        elif event_type == pygame.MOUSEBUTTONUP:
            self.mouse_up(coords)

    def mouse_move(self, coords):
        for button in self.buttons:
            if button.rect.collidepoint(coords):
                button.color = 'light gray'
            else:
                button.color = 'white'

    def mouse_down(self, coords):
        for button in self.buttons:
            if button.rect.collidepoint(coords):
                button.color = 'gray'

    def mouse_up(self, coords):
        for button in self.buttons:
            if button.rect.collidepoint(coords):
                button.on_click(self)
                button.color = 'light gray'

        if len(self.holes) == self.holes_limit:
            self.holes.pop(0)
        self.holes.append(Hole(coords, self.surface))
