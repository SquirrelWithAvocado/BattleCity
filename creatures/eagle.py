import pygame
from creatures.creature import Creature

class Eagle(Creature):
    def __init__(
        self, 
        surface, 
        pos, 
        image=r'images\eagle1.png',
    ):
        self.is_alive = True
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.health = 1
        self.name = 'Eagle'
        self.surface = surface

    def update(self):
        self.surface.blit(self.image, self.rect)
        if self.health <= 0:
            self.is_alive = False