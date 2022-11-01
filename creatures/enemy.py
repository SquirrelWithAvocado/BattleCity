import pygame
import random

from bullet import Bullet
from constants import (
    GENERAL_ROTATE_ANGLES as rotate_angles,
    ENEMY_SPEED,
    DIRECTIONS_LIST as directions,
    DIRECTION_DICT as direction_dict,
)
from creatures.creature import Creature


class Enemy(Creature):

    def __init__(
            self,
            surface,
            pos,
            tilemap,
            player,
            eagle,
            bullets,
            respawn_time,
            enemies,
            enemy_type,
            image_path=r'images\enemy_tank_.png',
            speed=ENEMY_SPEED,
    ):
        self.enemy_type = enemy_type
        super().__init__(
            len(enemies),
            'Enemy',
            surface,
            pos,
            tilemap,
            image_path,
            speed,
            health=1
        )

        self.enemy_type = enemy_type
        self.enemies = enemies
        self.damage = 1

        self.respawn_time = respawn_time
        self.cur_time = 0
        self.period = self.respawn_time / 8

        self.shoot_delay = 30
        self.player = player
        self.eagle = eagle
        self.bullets = bullets

    def move(self):
        if self.check_screen_border():
            self.invert_direction()
        self.change_direction()
        self.rect.move_ip(self.direction[0], self.direction[1])
        x, y = self.process_rotate_coords()
        self.rotate(rotate_angles[x, y])
        self.check_collisions()

    def process_rotate_coords(self):
        x = self.direction[0]
        y = self.direction[1]

        if self.direction[0] != 0:
            x //= abs(self.direction[0])
        if self.direction[1] != 0:
            y //= abs(self.direction[1])

        return x, y

    def change_direction(self):
        if random.randint(1, 2) % 2 == 0:
            if self.cur_time < self.period:
                if self.cur_time % 40 == 0:
                    self.set_rnd_dir()
                    self.on_tile_reach()
            elif self.player.is_alive and self.cur_time < 2 * self.period:
                self.move_to(self.player)
            else:
                self.cur_time = self.period
                self.move_to(self.eagle)

    def set_rnd_dir(self):
        self.direction = directions[random.randint(0, 3)]

    def on_tile_reach(self):
        x, y = self.rect.topleft
        if x % 8 == 0 and y % 8 == 0 and random.randint(1, 16) % 16 == 0:
            self.change_direction()

    def move_to(self, obj):
        x, y = obj.rect.topleft
        ex, ey = self.rect.topleft

        distance_x = abs(x - ex)
        distance_y = abs(y - ey)

        if distance_x > 10:
            dx = (x - ex) / distance_x
            self.direction = [dx * self.speed, 0]

        elif distance_y > 10:
            dy = (y - ey) / distance_y
            self.direction = [0, dy * self.speed]

    def check_collisions(self):
        if self.check_tile_collision():
            self.set_rnd_dir()
        self.check_player_collision()
        self.check_another_enemy_collision()

    def check_player_collision(self):
        if self.rect.colliderect(self.player.rect):
            if self.process_collisions(self.player):
                self.set_rnd_dir()

    def check_another_enemy_collision(self):
        for enemy in self.enemies:
            if self.rect.colliderect(enemy.rect):
                if self.process_collisions(enemy):
                    self.set_rnd_dir()

    def invert_direction(self):
        self.direction = [-self.direction[0], -self.direction[1]]

    def shoot(self):
        if self.shoot_turn == 1:
            px, py = self.px1, self.py1
        else:
            px, py = self.px2, self.py2
        self.shoot_turn *= -1

        self.bullets.append(
            Bullet(self, px, py, self.direction, self.damage, self.surface)
        )

    def update(self):
        if self.health <= 0:
            self.is_alive = False

        self.direction = [int(self.direction[0]), int(self.direction[1])]
        self.cur_time += 1

        if self.shoot_timer <= 0:
            self.process_bullet_dir()
            self.shoot()
            self.shoot_timer = self.shoot_delay

        self.move()

        self.surface.blit(self.image, self.rect)
        self.shoot_timer -= 1
