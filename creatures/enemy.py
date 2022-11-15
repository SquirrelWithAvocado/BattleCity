import pygame
import random

from bullet import Bullet
from constants import (
    GENERAL_ROTATE_ANGLES as rotate_angles,
    ENEMY_SPEED,
    DIRECTIONS_LIST as directions,
    DIRECTION_DICT as direction_dict,
    LIGHT_TANK_STAT,
    RAPID_TANK_STAT,
    SHOOTER_TANK_STAT,
    HEAVY_TANK_STAT
)
from creatures.EnemyType import EnemyType
from creatures.creature import Creature


class Enemy(Creature):

    def __init__(
            self,
            surface,
            pos,
            tile_map,
            player,
            eagle,
            bullets,
            respawn_time,
            enemies,
            enemy_type,
    ):
        self.enemy_type = enemy_type

        self.enemies = enemies
        self.damage = 1

        self.respawn_time = respawn_time
        self.cur_time = 0
        self.period = self.respawn_time / 8

        self.health, self.speed, self.shoot_delay, self.img_path, self.points = self.choose_class()

        super().__init__(
            len(enemies),
            'Enemy',
            surface,
            pos,
            tile_map,
            self.img_path,
            self.speed,
            self.health
        )

        self.player = player
        self.eagle = eagle
        self.bullets = bullets

    def choose_class(self):
        if self.enemy_type == EnemyType.LightTank:
            return LIGHT_TANK_STAT
        elif self.enemy_type == EnemyType.RapidTank:
            return RAPID_TANK_STAT
        elif self.enemy_type == EnemyType.ShooterTank:
            return SHOOTER_TANK_STAT
        elif self.enemy_type == EnemyType.HeavyTank:
            return HEAVY_TANK_STAT

    def move(self):
        if self.check_screen_border():
            self.invert_direction()

        for concrete in self.tilemap.tiles_dict['concrete']:
            if self.rect.colliderect(concrete.rect):
                self.invert_direction()

        self.change_direction()
        self.rect.move_ip(self.direction[0] * self.speed, self.direction[1] * self.speed)
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

        if self.cur_time % 40 > 30:
            if distance_x > 10:
                dx = int((x - ex) / distance_x)
                self.direction = [dx, 0]
        else:
            if distance_y > 10:
                dy = int((y - ey) / distance_y)
                self.direction = [0, dy]

    def check_collisions(self):
        self.check_tile_collision()
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
                    return True

    def invert_direction(self):
        self.direction = [-self.direction[0], -self.direction[1]]

    def shoot(self):
        if self.shoot_turn == 1:
            px, py = self.px1, self.py1
        else:
            px, py = self.px2, self.py2

        coords = (px, py)
        self.shoot_turn *= -1

        self.bullets.append(
            Bullet(
                self,
                coords,
                self.direction,
                self.damage,
                self.surface,
                self.tilemap,
                self.enemies,
                self.player,
                self.eagle,
                False
            )
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
