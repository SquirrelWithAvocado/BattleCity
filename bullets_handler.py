import pygame 
from bullet import Bullet
from creatures.enemy import Enemy
from creatures.player import Player

class BulletsHandler:
    def __init__(self, enemies, player):
        self.bullets = []
        self.enemies = enemies
        self.player = player
    
    def update_bullets(self):
        for bullet in self.bullets:
                self.update_tile_bullet_collisions(bullet)
                
                if bullet.parent.name == "Player":
                    self.update_player_bullet_collisions(bullet)
                
                if bullet.parent.name == "Enemy":
                    self.update_enemy_bullet_collisions(bullet)
                        
                bullet.update()
        
    def update_player_bullet_collisions(self, bullet):
        for enemy in self.enemies:
            if bullet.rect.colliderect(enemy.rect):
                enemy.health -= bullet.damage
                if (bullet in self.bullets):
                    self.bullets.remove(bullet)
            if bullet.rect.colliderect(self.eagle.rect):
                self.bullets.remove(bullet)
    
    def update_enemy_bullet_collisions(self, bullet):
        if bullet.rect.colliderect(self.player.rect):
            self.player.health -= 1
            self.bullets.remove(bullet)
        elif bullet.rect.colliderect(self.eagle.rect):
            self.eagle.health -= 1
            self.bullets.remove(bullet)
    
    def update_tile_bullet_collisions(self, bullet):
        for tile in self.tilemap.walls:
            if bullet.rect.colliderect(tile.rect) and bullet in self.bullets and tile in self.tilemap.walls:                
                self.tilemap.walls.remove(tile)
                self.bullets.remove(bullet)
                x, y = tile.rect.topleft[1] // 26, tile.rect.topleft[0] // 26 
                self.tilemap.map[x][y] = '0'
                self.tilemap.load_tiles()
                self.tilemap.load_map()