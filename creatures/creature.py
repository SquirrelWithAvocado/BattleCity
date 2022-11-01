import pygame
from pygame.locals import *
from bullet import Bullet
from constants import DIRECTION_DICT as direction_dict


class Creature(pygame.sprite.Sprite):
    """Player functionality"""

    def __init__(
            self,
            id,
            name,
            surface,
            pos,
            tilemap,
            image_path,
            speed,
            health=1
    ):
        self.health = health
        self.is_alive = True

        self.name = name
        self.id = id

        self.direction = [0, -1]
        self.surface = surface
        self.screen_size = surface.get_size()
        self.render(image_path)

        self.rect.topleft = pos
        self.speed = speed
        self.tilemap = tilemap

        self.shoot_delay = 30
        self.shoot_timer = 0
        self.shoot_turn = 1

        self.collision_tolerance = 10

    def render(self, image_path):
        self.angle = 0
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

    def rotate(self, angle):
        d_angle = angle - self.angle
        self.angle += d_angle
        self.direction = direction_dict[self.angle]
        self.image = pygame.transform.rotate(self.image, d_angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def check_tile_collision(self):
        for tile in self.tilemap.tiles:
            if self.rect.colliderect(tile.rect) and tile.name != "grass":
                return self.process_collisions(tile)

    def process_collisions(self, obj):
        on_collision = False
        if abs(self.rect.top - obj.rect.bottom) < self.collision_tolerance:
            self.rect.top = obj.rect.bottom
            on_collision = True
        if abs(self.rect.bottom - obj.rect.top) < self.collision_tolerance:
            self.rect.bottom = obj.rect.top
            on_collision = True
        if abs(self.rect.right - obj.rect.left) < self.collision_tolerance:
            self.rect.right = obj.rect.left
            on_collision = True
        if abs(self.rect.left - obj.rect.right) < self.collision_tolerance:
            self.rect.left = obj.rect.right
            on_collision = True
        return on_collision

    def check_screen_border(self):
        on_border = False
        if self.rect.left < 0:
            self.rect.left = 0
            on_border = True
        if self.rect.right > self.screen_size[0]:
            self.rect.right = self.screen_size[0]
            on_border = True
        if self.rect.top <= 0:
            self.rect.top = 0
            on_border = True
        if self.rect.bottom >= self.screen_size[1]:
            self.rect.bottom = self.screen_size[1]
            on_border = True
        return on_border

    def process_bullet_dir(self):
        if abs(self.direction[0]) == 1:
            self.py1, self.py2 = self.rect.center[1] - 8, self.rect.center[1] + 5
            self.px1 = self.px2 = self.rect.center[0] + 20 * self.direction[0]
        if abs(self.direction[1]) == 1:
            self.px1, self.px2 = self.rect.center[0] - 8, self.rect.center[0] + 5
            self.py1 = self.py2 = self.rect.center[1] + 20 * self.direction[1]
