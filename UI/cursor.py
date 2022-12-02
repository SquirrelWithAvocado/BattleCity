import pygame


class Cursor:
    def __init__(self):

        big_image = pygame.image.load(r'images/UI images/cursor_2.png').convert_alpha()

        self.cursor_shift = -20
        self.cursor = pygame.transform.scale(big_image, (40, 40))

        pygame.mouse.set_visible(False)

    def update(self, coords, surface):
        surface.blit(self.cursor, (coords[0] + self.cursor_shift, coords[1] + self.cursor_shift))
