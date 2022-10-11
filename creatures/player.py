from matplotlib import collections
import pygame
from pygame.locals import *
from bullet import Bullet
from creatures.creature import Creature

class Player(Creature):
    """Player functionality"""

    def __init__(
        self, 
        surface, 
        pos, 
        tilemap,
        image=r'images\player_tank1.2.png',
        speed=5, 
    ):
        super().__init__(
            surface, 
            pos, 
            tilemap,
            image,
            speed,
            health=1 
        )

        self.name = 'Player'
        self.enemies = []

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

    def move(self, pressed_key):
        self.rect.move_ip(self.key_controls[pressed_key])
        self.rotate(pressed_key)
        self.check_collisions()
        self.check_screen_border()

    def check_collisions(self):
        for tile in self.tilemap.tiles:
            if self.rect.colliderect(tile.rect) and tile.name != "grass":
                self.collisions(tile, collision_tolerance=10)
    
    def ckeck_enemy_collision(self):
        for enemy in self.enemies:
            if self.rect.colliderect(enemy.rect):
                self.collisions(enemy, collision_tolerance=10)
    
    def collisions(self, obj, collision_tolerance):
        if abs(self.rect.top - obj.rect.bottom) < collision_tolerance:
            self.rect.top = obj.rect.bottom
        if abs(self.rect.bottom - obj.rect.top) < collision_tolerance:
            self.rect.bottom = obj.rect.top
        if abs(self.rect.right - obj.rect.left) < collision_tolerance:
            self.rect.right = obj.rect.left
        if abs(self.rect.left - obj.rect.right) < collision_tolerance:
            self.rect.left= obj.rect.right

    def rotate(self, key):
        self.dalgle = self.rotate_angles[key] - self.angle
        self.angle += self.dalgle
        self.direction = self.direction_dict[self.angle]
        self.image = pygame.transform.rotate(self.image, self.dalgle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.process_bullet_dir()
        self.surface.blit(self.image, self.rect)
        self.shoot_timer -= 1
    
    def shoot(self):
        if self.shoot_timer <= 0:
            self.shoot_timer = self.shoot_delay
            if self.shoot_turn == 1:
                px, py = self.px1, self.py1
            else:
                px, py = self.px2, self.py2
            self.shoot_turn *= -1
            return Bullet(self, px, py, self.direction, 1, self.surface)   
    
    def process_bullet_dir(self):
        if abs(self.direction[0]) == 1:
            self.py1, self.py2 = self.rect.center[1] - 8, self.rect.center[1] + 5
            self.px1 = self.px2 = self.rect.center[0] + 20 * self.direction[0]
        if abs(self.direction[1]) == 1:
            self.px1, self.px2 = self.rect.center[0] - 8, self.rect.center[0] + 5
            self.py1 = self.py2 = self.rect.center[1] + 20 * self.direction[1]