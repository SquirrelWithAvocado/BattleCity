import pygame
from bullet import Bullet
from creatures.creature import Creature
from constants import (
    KEY_CONTROLS as keys,
    ROTATE_ANGLES as rotate_angles,
    DIRECTION_DICT as direction_dict
)


class Player(Creature):
    """Player functionality"""

    def __init__(
            self,
            surface,
            pos,
            tilemap,
            enemies,
            image=r'images\player_tank1.2.png',
            speed=5,
            hearts=2
    ):
        super().__init__(
            0,
            'Player',
            surface,
            pos,
            tilemap,
            image,
            speed,
            health=1
        )

        self.enemies = enemies
        self.score = 0
        self.hearts = hearts

    def move(self, pressed_key):
        self.rect.move_ip(keys[pressed_key])
        self.rotate(rotate_angles[pressed_key])
        self.check_collisions()

    def check_collisions(self):
        self.check_tile_collision()
        self.check_enemy_collision()
        self.check_screen_border()

    def check_enemy_collision(self):
        for enemy in self.enemies:
            if self.rect.colliderect(enemy.rect):
                self.process_collisions(enemy)

    def shoot(self):
        if self.shoot_timer <= 0:
            self.shoot_timer = self.shoot_delay
            if self.shoot_turn == 1:
                px, py = self.px1, self.py1
            else:
                px, py = self.px2, self.py2
            self.shoot_turn *= -1
            return Bullet(self, px, py, self.direction, 1, self.surface)

    def respawn(self):
        self.hearts -= 1
        self.is_alive = True
        self.health = 1
        self.rect.center = (320, 550)

    def update(self):
        if self.health <= 0:
            self.is_alive = False
            if self.hearts > 0:
                self.respawn()

        self.process_bullet_dir()
        self.surface.blit(self.image, self.rect)
        self.shoot_timer -= 1
