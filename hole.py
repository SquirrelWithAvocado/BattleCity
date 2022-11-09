import pygame


class Hole:
    def __init__(self, pos, surface):
        big_image = pygame.image.load(r'images\bullet_hole.png').convert_alpha()
        self.image = pygame.transform.scale(big_image, (40, 40))
        self.pos = pos
        self.surface = surface

    def draw(self):
        self.surface.blit(self.image, self.pos)