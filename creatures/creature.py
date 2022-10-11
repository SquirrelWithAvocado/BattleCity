from matplotlib import collections
import pygame
from pygame.locals import *
from bullet import Bullet

class Creature(pygame.sprite.Sprite):
    """Player functionality"""

    def __init__(
        self, 
        surface, 
        pos, 
        tilemap,
        image,
        speed,
        health=1
    ):
        self.health = health

        self.direction = [0, -1]
        self.surface = surface
        self.screen_size = surface.get_size()
        self.render(image)

        self.rect.center = pos
        self.speed = speed
        self.tilemap = tilemap

        self.direction_dict = {
            0: (0, -1),
            180: (0, 1),
            90: (-1, 0),
            270: (1, 0)
        }

        self.shoot_delay = 30
        self.shoot_timer = 0
        self.shoot_turn = 1

    def render(self, image):
        self.angle = 0
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

    def check_collisions(self):
        collision_tolerance = 10
        for tile in self.tilemap.tiles:
            if self.rect.colliderect(tile.rect) and tile.name != "grass":
                if abs(self.rect.top - tile.rect.bottom) < collision_tolerance:
                    self.rect.top = tile.rect.bottom
                if abs(self.rect.bottom - tile.rect.top) < collision_tolerance:
                    self.rect.bottom = tile.rect.top
                if abs(self.rect.right - tile.rect.left) < collision_tolerance:
                    self.rect.right = tile.rect.left
                if abs(self.rect.left - tile.rect.right) < collision_tolerance:
                    self.rect.left= tile.rect.right

    def check_screen_border(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_size[0]:
            self.rect.right = self.screen_size[0]
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.screen_size[1]:
            self.rect.bottom = self.screen_size[1]

 
