import pygame, random
from pygame.locals import *
from TileMap import tilemap
from creatures.player import Player
from creatures.easy_enemy import Easy_enemy
from creatures.eagle import Eagle
from TileMap import *

class Battlefield:
    """Game battlefield"""

    def __init__(self, screen, level):
        pygame.init()
        self.player_count = 1
        self.level = level
        self.screen = screen
        self.game_surface = pygame.Surface((676, 676))
        self.running = True
        self.clock = pygame.time.Clock()
        self.spawn_points = [(130, 30), (470, 30)]
        self.spawn_point = 0

        self.caption = "Battlecity: battlefield"
        pygame.display.set_caption(self.caption)
        
        self.spriteset = Spriteset(r'TileMap\spriteset1.png')
        self.tilemap = Tilemap(fr'TileMap\maps\map_{self.level}.csv', self.spriteset, self.game_surface)
        self.eagle = Eagle(self.game_surface, (338, 651))
        self.bullets = []
        self.enemies = []
        self.player = Player(self.game_surface, (320, 550), self.tilemap)
        self.enemy_limit = 10
        self.enemy_respawn_time = (190 - self.level * 4 - (self.player_count - 1) * 20) * 60
        self.respawn_timer = self.enemy_respawn_time / 30
        
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

            self.tilemap.update_map()
            if self.player.is_alive:
                self.player.update()

            if self.eagle.is_alive:
                self.eagle.update()
            self.update_enemies()

            self.update_bullets()
            self.respawn_timer += 1

            self.screen.blit(self.game_surface, (50, 50))
            pygame.display.update()

            self.clock.tick(30)

    def update_enemies(self):
        print(f'\r{self.respawn_timer} :self.enemy_respawn_time{self.enemy_respawn_time}')
        if self.respawn_timer >= self.enemy_respawn_time / 30 and self.enemy_limit > 0:
            self.respawn_timer = 0
            self.enemy_limit -= 1
            self.enemies.append(
                Easy_enemy(
                    self.game_surface, 
                    self.spawn_points[self.spawn_point], 
                    self.tilemap, 
                    self.player, 
                    self.eagle,
                    self.bullets, 
                    self.enemy_respawn_time, 
                    len(self.enemies),
                    self.enemies
                )   
            )
            self.spawn_point = (self.spawn_point + 1) % 2
        
        for enemy in self.enemies:
            if not(enemy.is_alive):
                self.enemies.remove(enemy)
            enemy.update()

    def update_bullets(self):
        for bullet in self.bullets:
                for tile in self.tilemap.walls:
                    if bullet.rect.colliderect(tile.rect) and bullet in self.bullets and tile in self.tilemap.walls:                
                        self.tilemap.walls.remove(tile)
                        self.bullets.remove(bullet)
                        x, y = tile.rect.topleft[1] // 26, tile.rect.topleft[0] // 26 
                        self.tilemap.map[x][y] = '0'
                        self.tilemap.load_tiles()
                        self.tilemap.load_map()
                
                if bullet.parent.name == "Player":
                    for enemy in self.enemies:
                        if bullet.rect.colliderect(enemy.rect):
                            enemy.health -= bullet.damage
                            if (bullet in self.bullets):
                                self.bullets.remove(bullet)
                        if bullet.rect.colliderect(self.eagle.rect):
                            self.bullets.remove(bullet)
                
                if bullet.parent.name == "Enemy":
                    if bullet.rect.colliderect(self.player.rect):
                        self.player.health -= 1
                        self.bullets.remove(bullet)
                    if bullet.rect.colliderect(self.eagle.rect):
                            self.eagle.health -= 1
                            self.bullets.remove(bullet)
                        
                bullet.update()

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
