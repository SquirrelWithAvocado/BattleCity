import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    """Player functionality"""

    def __init__(
        self, 
        screen, 
        pos, 
        image=r'images\player_tank1.png',
        speed=5
    ):
        self.screen = screen
        self.screen_size = screen.get_size()
        self.render(image)

        self.rect.center = pos
        self.speed = speed


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
    
    def render(self, image):
        self.angle = 0
        self.image = pygame.image.load(image)
        self.image.convert()

        self.rect = self.image.get_rect()

    def move(self, pressed_key):
        self.rect.move_ip(self.key_controls[pressed_key])
        self.rotate(pressed_key)
        self.check_screen_border()

    def rotate(self, key):
        self.dalgle = self.rotate_angles[key] - self.angle
        self.angle += self.dalgle
        self.image = pygame.transform.rotate(self.image, self.dalgle)

    def check_screen_border(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_size[0]:
            self.rect.right = self.screen_size[0]
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.screen_size[1]:
            self.rect.bottom = self.screen_size[1]

    def update(self):
        self.screen.blit(self.image, self.rect)

    def flip(self, x, y):
        if not(self.rotation[0] and x):
            self.surf = pygame.transform.flip(self.surf, x, y)
        if not(self.rotation[1] and y):
            self.surf = pygame.transform.flip(self.surf, x, y)