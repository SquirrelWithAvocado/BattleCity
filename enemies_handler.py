import pygame
from creatures.enemy import Enemy, EnemyType

class EnemiesHandler:
    def __init__(self, player, eagle, surface, limit, level, tilemap):
        self.player = player
        self.eagle = eagle
        self.game_surface = surface
        self.level = level
        self.tilemap = tilemap

        self.players_count = 1

        self.enemy_respawn_time = (190 - self.level * 4 - (self.players_count - 1) * 20) * 60
        self.respawn_timer = self.enemy_respawn_time / 30
        self.enemies_spawned = 0
        self.enemies = []
        self.enemy_limit = limit

        self.spawn_points = [(130, 30), (470, 30)]
        self.spawn_point = 0
    
    def update_enemies(self):
        print(f'\r{self.respawn_timer} :self.enemy_respawn_time{self.enemy_respawn_time}', end="")
        if self.respawn_timer >= self.enemy_respawn_time / 30 and self.enemy_limit > 0:
            self.respawn_timer = 0
            self.enemy_limit -= 1 
            self.enemies.append(self.spawn_enemy())
            self.enemies_spawned += 1
            self.spawn_point = (self.spawn_point + 1) % 2
        
        for enemy in self.enemies:
            if not(enemy.is_alive):
                self.enemies.remove(enemy)
                self.enemy_icons.pop()
                self.player.score += 100 * enemy.enemy_type
            enemy.update()
    
    def spawn_enemy(self):
        return Enemy(
            self.game_surface, 
            self.spawn_points[self.spawn_point], 
            self.tilemap, 
            self.player, 
            self.eagle,
            self.enemies_spawned,
            self.enemy_respawn_time,
            self.enemies,
            EnemyType.LightEnemy
        )  