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
        image=r'images\enemy_tank.png',
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

        self.name = 'Enemy'
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.shoot_delay = 30
        self.player = player
        self.choose_rnd_destination()

        self.rotate_angles = {
            (0, -1): 0,
            (0, 1): 180,
            (-1, 0): 90,
            (1, 0): 270,
        }   
    
    def move(self):
        if self.rect.x - self.destination[0] > 0:
            self.rect.move_ip(-1, 0)
            self.direction = [-1, 0]
        elif self.rect.x - self.destination[0] < 0:
            self.rect.move_ip(1, 0)
            self.direction = [1, 0]
        elif self.rect.y - self.destination[1] > 0:
            self.rect.move_ip(0, -1)
            self.direction = [0, -1]
        elif self.rect.y - self.destination[1] < 0:
            self.direction = [0, 1]
        self.rotate()
        self.check_collisions()
        
    def choose_rnd_destination(self):
        rnd_int = random.randint(0, len(self.tilemap.grass) - 1)
        self.destination = [self.tilemap.grass[rnd_int].rect.y, self.tilemap.grass[rnd_int].rect.x]
    
    def check_collisions(self):
        for tile in self.tilemap.tiles:
            if self.rect.colliderect(tile.rect) and tile.name != "grass":
                self.collisions(tile, collision_tolerance=10)
    
    def ckeck_player_collision(self):
            if self.rect.colliderect(self.player.rect):
                self.collisions(self.player, collision_tolerance=10)
    
    def collisions(self, obj, collision_tolerance):
        if abs(self.rect.top - obj.rect.bottom) < collision_tolerance:
            self.rect.top = obj.rect.bottom
        if abs(self.rect.bottom - obj.rect.top) < collision_tolerance:
            self.rect.bottom = obj.rect.top
        if abs(self.rect.right - obj.rect.left) < collision_tolerance:
            self.rect.right = obj.rect.left
        if abs(self.rect.left - obj.rect.right) < collision_tolerance:
            self.rect.left= obj.rect.right
    
    def rotate(self):
        self.dalgle = self.rotate_angles[(self.direction[0], self.direction[1])] - self.angle
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

        return Bullet(self, px, py, self.direction, 1, self.surface)   
    
    def process_bullet_dir(self):
        if abs(self.direction[0]) == 1:
            self.py1, self.py2 = self.rect.center[1] - 4, self.rect.center[1] + 3
            self.px1 = self.px2 = self.rect.center[0] + 20 * self.direction[0]
        if abs(self.direction[1]) == 1:
            self.px1, self.px2 = self.rect.center[0] - 4, self.rect.center[0] + 3
            self.py1 = self.py2 = self.rect.center[1] + 20 * self.direction[1]

    def update(self):
        self.process_bullet_dir()
        if self.shoot_timer <= 0:
            self.shoot()
            self.shoot_timer = self.shoot_delay
            self.choose_rnd_destination()
        self.move()    
        self.surface.blit(self.image, self.rect)
        self.shoot_timer -= 1
        
