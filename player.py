from matplotlib import collections
import pygame
from pygame.locals import *
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    """Player functionality"""

    def __init__(
        self, 
        surface, 
        pos, 
        tilemap,
        image=r'images\player_tank1.2.png',
        speed=5, 
    ):
        self.direction = [0, 0]
        self.surface = surface
        self.screen_size = surface.get_size()
        self.render(image)

        self.rect.center = pos
        self.speed = speed
        self.tilemap = tilemap

        self.key_controls = {
            K_w: (0, -self.speed),
            K_s: (0, self.speed),
            K_a: (-self.speed, 0),
            K_d: (self.speed, 0),

            K_UP: (0, -self.speed),
            K_DOWN: (0, self.speed),
            K_LEFT: (-self.speed, 0),
            K_RIGHT: (self.speed, 0)
        }

        self.rotate_angles = {
            K_w: 0,
            K_s: 180,
            K_a: 90,
            K_d: 270,

            K_UP: 0,
            K_DOWN: 180,
            K_LEFT: 90,
            K_RIGHT: 270
        }   

        self.direction_dict = {
            0: (0, -1),
            180: (0, 1),
            90: (-1, 0),
            270: (1, 0)
        }

        self.shoot_delay = 240
        self.shoot_timer = 0
        self.shoot_turn = 1
    
    def process_bullet_dir(self):
        if abs(self.direction[0]) == 1:
            self.py1, self.py2 = self.rect.center[1] - 8, self.rect.center[1] + 5
            self.px1 = self.px2 = self.rect.center[0] + 20 * self.direction[0]
        if abs(self.direction[1]) == 1:
            self.px1, self.px2 = self.rect.center[0] - 8, self.rect.center[0] + 5
            self.py1 = self.py2 = self.rect.center[1] + 20 * self.direction[1]

    def render(self, image):
        self.angle = 0
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

    def move(self, pressed_key):
        self.rect.move_ip(self.key_controls[pressed_key])
        self.rotate(pressed_key)
        self.check_collisions()
        self.check_screen_border()

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

    def rotate(self, key):
        self.dalgle = self.rotate_angles[key] - self.angle
        self.angle += self.dalgle
        self.direction = self.direction_dict[self.angle]
        self.image = pygame.transform.rotate(self.image, self.dalgle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def check_screen_border(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_size[0]:
            self.rect.right = self.screen_size[0]
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.screen_size[1]:
            self.rect.bottom = self.screen_size[1]

    def shoot(self):
        if self.shoot_timer <= 0:
            self.shoot_timer = self.shoot_delay
            if self.shoot_turn == 1:
                px, py = self.px1, self.py1
            else:
                px, py = self.px2, self.py2
            self.shoot_turn *= -1
            return Bullet(self, px, py, self.direction, 1, self.surface)    

    def update(self):
        self.process_bullet_dir()
        self.surface.blit(self.image, self.rect)
        self.shoot_timer -= 1

