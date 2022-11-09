import pygame

from UI.text import Text


class SideMenu:
    def __init__(self, player, screen, enemy_limit):
        self.enemy_icon = pygame.image.load(r'images/enemy_tank.png')
        self.heart_img = pygame.image.load(r'images/heart.png')
        self.enemy_limit = enemy_limit
        self.player = player
        self.screen = screen
        self.enemy_icons = list()

        self.load_enemy_icon()

    def load_enemy_icon(self):
        for i in range(self.enemy_limit):
            self.enemy_icons.append(self.enemy_icon.copy())

    def update(self):
        Text(f"Score: {self.player.score}", (100, 756), fontsize=32, color='white').draw(self.screen)
        self.screen.blit(self.heart_img, (60, 780))
        Text(f": {self.player.hearts}", (120, 795), fontsize=50, color='white').draw(self.screen)

        self.update_icons()

    def update_icons(self):
        for i in range(len(self.enemy_icons)):
            self.screen.blit(self.enemy_icons[i], (170 + i % 5 * 20, 747 + i // 5 * 20))
