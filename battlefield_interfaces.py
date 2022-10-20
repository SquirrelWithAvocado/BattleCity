import pygame
from text import Text

class SideInterface:
    def __init__(self, surface):
        self.heart_img = pygame.image.load(r'images\heart1.png')
        self.enemy_icon = pygame.image.load(r'images\enemy_tank15.png')
        self.enemy_limit = 10

        self.load_enemy_icon()
        self.captions = []
        self.surface = surface
        
    def set_captions(self):
        Text(f"Score: {self.player.score}", (100, 756), fontsize=32).draw(self.surface)
        Text(f": {self.player.hearts}", (120, 795), fontsize=50).draw(self.surface)
    
    def load_enemy_icon(self):
        self.enemy_icons = []
        for i in range(self.enemy_limit):
            self.enemy_icons.append(pygame.image.load('images\enemy_tank15.png'))

    def update_icons(self):
        for i in range(len(self.enemy_icons)):
                self.surface.blit(self.enemy_icons[i], (170 + i % 5 * 20, 747 + i // 5 * 20))
    
    def update(self):
        self.update_icons()
        self.surface.blit(self.heart_img, (60, 780))
        