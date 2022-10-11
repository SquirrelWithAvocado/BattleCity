import pygame, csv, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, coords, spriteset):
        self.img = spriteset.parse_sprite(image)
        self.name = image.replace('.png', '')
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = coords
        self.size = 50

    def draw(self, surface):
        surface.blit(self.img, (self.rect.x, self.rect.y))
