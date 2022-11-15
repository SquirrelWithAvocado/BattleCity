import pygame


class Cursor:
    def __init__(self, surface):
        self.surface = surface

        big_image = pygame.image.load(r'images/UI images/cursor_2.png').convert_alpha()

        self.cursor_shift = 20
        self.cursor = pygame.transform.scale(big_image, (40, 40))

        pygame.mouse.set_visible(False)

    def update(self, coords):
        self.surface.blit(self.cursor, (coords[0], coords[1]))
