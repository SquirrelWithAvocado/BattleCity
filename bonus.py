import random
import pygame


class Bonus:
    def __init__(self, surface, player):
        self.image = pygame.image.load(r'images\speed_bonus.png')
        self.rect = self.image.get_rect()
        self.surface = surface
        self.player = player

        self.picked = False
        self.timer = 30
        self.spawn()

    def on_pick(self):
        if not self.picked:
            self.player.speed += 2
            self.picked = True
        else:
            if self.timer <= 0:
                self.player.speed = self.player.nominal_speed
            else:
                self.timer -= 1

    def spawn(self):
        size = self.surface.get_rect().size
        self.rect.center = (random.randint(0, size[0]), random.randint(0, size[1]))

    def update(self):
        if not self.picked:
            self.surface.blit(self.image, self.rect)
        else:
            self.on_pick()
