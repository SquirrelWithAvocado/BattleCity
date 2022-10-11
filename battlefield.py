import pygame
from pygame.locals import *
from player import Player
from TileMap import *

class Battlefield:
    """Game battlefield"""

    def __init__(self, screen):
        pygame.init()
        self.screen = screen
        self.game_surface = pygame.Surface((650, 650))
        self.running = True
        self.clock = pygame.time.Clock()
 
        self.caption = "Battlecity: battlefield"
        pygame.display.set_caption(self.caption)

        self.spriteset = Spriteset(r'TileMap\spriteset1.png')
        self.tilemap = Tilemap(r'TileMap\maps\map_2.csv', self.spriteset, self.game_surface)
        self.player = Player(self.game_surface, (50, 50), self.tilemap)
        self.bullets = []
        

    def run(self):
        "Battlefield event loop"
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    continue

            self.check_keys()

            self.screen.fill(Color('gray'))

            self.screen.blit(self.game_surface, (50, 50))
            self.tilemap.update_map()
            self.player.update()
            
            for bullet in self.bullets:
                for tile in self.tilemap.walls:
                    if bullet.rect.colliderect(tile):
                        self.bullets.remove(bullet)
                bullet.update()

            pygame.display.update()

            self.clock.tick(30)

    def check_keys(self):
        self.pressed_keys = pygame.key.get_pressed()

        for key in self.player.key_controls:
            if self.pressed_keys[K_SPACE]:
                bul = self.player.shoot()
                if bul != None:
                    self.bullets.append(bul)
            if self.pressed_keys[key]:
                self.player.move(key)
                break
