import pygame
from pygame.locals import *
from game_objects.bullet import Bullet
from game_objects.creatures.creature import Creature
from extra_modules.constants import ROTATE_ANGLES as rotate_angles
from extra_modules.animation_parsing_methods import parse_animation


class Player(Creature):
    """Player functionality"""

    def __init__(
            self,
            surface,
            pos,
            tile_map,
            enemies,
            bullets,
            eagle,
            bonuses,
            image=r'images\player animation\player_tank1.2.png',
            speed=5,
            hearts=0
    ):
        super().__init__(
            0,
            'Player',
            surface,
            pos,
            tile_map,
            image,
            speed,
            health=1
        )

        self.damage = 1
        self.bullets = bullets
        self.enemies = enemies
        self.bonuses = bonuses
        self.eagle = eagle
        self.score = 0
        self.hearts = hearts

        self.super_shooting_times = 0

        self.go_animation = parse_animation(r'images\player animation\animation_go.png')
        self.go_animation_counter = 0

        self.freeze_flag = False

        self.keys = {
            K_w: (0, -1),
            K_s: (0, 1),
            K_a: (-1, 0),
            K_d: (1, 0),
        }

    def move(self, pressed_key):
        self.go_animation_counter = (self.go_animation_counter + 1) % len(self.go_animation)
        self.angle = 0
        self.image = self.go_animation[self.go_animation_counter]
        self.rect.move_ip(
            self.keys[pressed_key][0] * self.speed,
            self.keys[pressed_key][1] * self.speed
        )
        self.rotate(rotate_angles[pressed_key])
        self.check_collisions()

    def check_collisions(self):
        self.check_tile_collision()
        self.check_ice_collisions()
        self.check_enemy_collision()
        self.check_bonus_collisions()
        self.check_screen_border()

    def check_bonus_collisions(self):
        for bonus in self.bonuses:
            if self.rect.colliderect(bonus.rect):
                bonus.on_pick()

    def check_enemy_collision(self):
        for enemy in self.enemies:
            if self.rect.colliderect(enemy.rect):
                self.process_collisions(enemy)

    def check_ice_collisions(self):
        for ice in self.tilemap.tiles_dict['ice']:
            if self.rect.colliderect(ice.rect) and not self.freeze_flag:
                self.freeze_flag = True
                self.speed -= 4
                break
        else:
            self.freeze_flag = False
            self.speed = self.nominal_speed

    def shoot(self):
        if self.shoot_timer <= 0:
            self.shoot_timer = self.shoot_delay
            if self.shoot_turn == 1:
                px, py = self.px1, self.py1
            else:
                px, py = self.px2, self.py2

            coords = (px, py)
            self.shoot_turn *= -1

            super_shooting = False
            if self.super_shooting_times > 0:
                self.super_shooting_times -= 1
                super_shooting = True

            shoot_sound = pygame.mixer.Sound(r'sound_effects/player_shoot.mp3')
            shoot_sound.set_volume(0.1)
            shoot_sound.play()

            return Bullet(
                self,
                coords,
                self.direction,
                self.damage,
                self.surface,
                self.tilemap,
                self.enemies,
                self,
                self.eagle,
                super_shooting
            )


    def respawn(self):
        self.hearts -= 1
        self.is_alive = True
        self.health = 1
        self.rect.center = (320, 550)

    def check_keys(self):
        pressed_keys = pygame.key.get_pressed()

        for key in self.keys:
            if pressed_keys[K_SPACE]:
                bullet = self.shoot()
                if bullet is not None:
                    self.bullets.append(bullet)
            if pressed_keys[key]:
                self.move(key)
                break

    def update(self):
        self.check_keys()

        if self.health <= 0:
            self.is_alive = False
            if self.hearts > 0:
                self.respawn()

        self.process_bullet_dir()
        self.surface.blit(self.image, self.rect)
        self.shoot_timer -= 1
