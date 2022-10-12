from matplotlib.widgets import EllipseSelector
import pygame, random
from pygame.locals import *
from creatures.creature import Creature
from bullet import Bullet

class Easy_enemy(Creature):

    def __init__(
        self, 
        surface, 
        pos, 
        tilemap,
        player,
        eagle,
        bullets,
        respawn_time,
        id,
        enemies,
        image=r'images\enemy_tank.png',
        speed=5, 
    ):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        super().__init__(
            surface, 
            pos, 
            tilemap,
            image,
            speed,
            health=1
        )

        self.name = 'Enemy'
        self.id = id
        self.speed = 1
        self.enemies = enemies

        self.respawn_time = respawn_time 
        self.cur_time = 0
        self.period = self.respawn_time / 8 


        self.shoot_delay = 30
        self.player = player
        self.eagle = eagle
        self.bullets = bullets

        self.rotate_angles = {
            (0, -1): 0,
            (0, 1): 180,
            (-1, 0): 90,
            (1, 0): 270,
        }   

        self.dir_list = [
            [-self.speed, 0],
            [self.speed, 0],
            [0, -self.speed],
            [0, self.speed]
        ]
    
    def move(self):
        self.check_screen_border()
        
        self.change_direction()
        self.rect.move_ip(self.direction[0], self.direction[1])
        self.rotate()
        self.check_collisions()
    
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
        self.direction = self.dir_list[random.randint(0, 3)]

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
        for tile in self.tilemap.tiles:
            if self.rect.colliderect(tile.rect) and tile.name != "grass":
                self.collisions(tile, collision_tolerance=10)
        self.check_player_collision()
        self.check_another_enemy_collision()
    
    def check_player_collision(self):
            if self.rect.colliderect(self.player.rect):
                self.collisions(self.player, collision_tolerance=10)
    
    def check_another_enemy_collision(self):
        for enemy in self.enemies:
            if self.rect.colliderect(enemy.rect):
                self.collisions(enemy, collision_tolerance=10)
    
    def collisions(self, obj, collision_tolerance):
        if abs(self.rect.top - obj.rect.bottom) < collision_tolerance:
            self.rect.top = obj.rect.bottom
            self.set_rnd_dir()
        if abs(self.rect.bottom - obj.rect.top) < collision_tolerance:
            self.rect.bottom = obj.rect.top
            self.set_rnd_dir()
        if abs(self.rect.right - obj.rect.left) < collision_tolerance:
            self.rect.right = obj.rect.left
            self.set_rnd_dir()
        if abs(self.rect.left - obj.rect.right) < collision_tolerance:
            self.rect.left= obj.rect.right
            self.set_rnd_dir()
        
    def invert_direction(self):
        self.direction = [-self.direction[0], -self.direction[1]]
    
    def rotate(self):
        x = self.direction[0]
        y = self.direction[1]

        if self.direction[0] != 0: x //= abs(self.direction[0]) 
        if self.direction[1] != 0: y //= abs(self.direction[1])

        self.dalgle = self.rotate_angles[x, y] - self.angle
        self.angle += self.dalgle
        self.direction = self.direction_dict[self.angle]
        self.image = pygame.transform.rotate(self.image, self.dalgle)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def shoot(self):
        if self.shoot_turn == 1:
            px, py = self.px1, self.py1
        else:
            px, py = self.px2, self.py2
        self.shoot_turn *= -1

        self.bullets.append(Bullet(self, px, py, self.direction, 1, self.surface))   
    
    def process_bullet_dir(self):
        if abs(self.direction[0]) == 1:
            self.py1, self.py2 = self.rect.center[1] - 6, self.rect.center[1] + 5
            self.px1 = self.px2 = self.rect.center[0] + 20 * self.direction[0]
        if abs(self.direction[1]) == 1:
            self.px1, self.px2 = self.rect.center[0] - 6, self.rect.center[0] + 5
            self.py1 = self.py2 = self.rect.center[1] + 20 * self.direction[1]

    def update(self):
        if self.health <= 0:
            self.is_alive = False 

        self.direction = [(int)(self.direction[0]), (int)(self.direction[1])]
        self.cur_time += 1 
        if self.shoot_timer <= 0:
            self.process_bullet_dir()
            self.shoot()
            self.shoot_timer = self.shoot_delay
        self.move()    
        self.surface.blit(self.image, self.rect)
        self.shoot_timer -= 1
        
    def check_screen_border(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.invert_direction()
        if self.rect.right > self.screen_size[0]:
            self.rect.right = self.screen_size[0]
            self.invert_direction()
        if self.rect.top <= 0:
            self.rect.top = 0
            self.invert_direction()
        if self.rect.bottom >= self.screen_size[1]:
            self.rect.bottom = self.screen_size[1]
            self.invert_direction()
