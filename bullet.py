import pygame, random

class Bullet:
    def __init__(self, parent, px, py, direction, damage, surface):
        self.surface = surface
        self.surface_size = surface.get_size()
        self.parent = parent
        self.image = pygame.image.load(r'images\bullet1.png')
        self.rect = self.image.get_rect()

        self.rect.center =  (px, py)
        self.damage = damage
        self.dx, self.dy = direction[0], direction[1]
        self.direction = direction

        self.speed = 10

        self.angle_dict = {
            (-1, 0): 90,
            (1, 0): -90,
            (0, -1): 0,
            (0, 1): 180
        }

        self.rotate()

    def update(self):
        self.move_bullet()
        self.surface.blit(self.image, self.rect)

    def move_bullet(self):
        self.rect.move_ip(self.dx * self.speed, self.dy * self.speed)

    def check_surface_border(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.surface_size[0]:
            self.rect.right = self.surface_size[0]
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.surface_size[1]:
            self.rect.bottom = self.surface_size[1]
    
    def rotate(self): 
        self.image = pygame.transform.rotate(self.image, self.angle_dict[self.direction])
        self.rect = self.image.get_rect(center=self.rect.center)