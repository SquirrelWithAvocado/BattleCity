import pygame
from pygame.locals import *

from creatures import (
    EnemyType,
    Player,
    Enemy,
    Eagle
)

from TileMap import Tilemap
from game_interfaces import SideMenu
from text import Text

from constants import (
    GAME_SURFACE_SIZE,
    SIDE_MENU_SIZE,
    GRAY,
)


class Battlefield:
    """Game battlefield"""

    def __init__(self, screen):
        pygame.init()

        self.level = 1
        self.player_count = 1
        self.enemy_spawn_order = 0

        self.game_surface = pygame.Surface(GAME_SURFACE_SIZE)

        self.screen = screen
        self.running = True
        self.game_over = False
        self.clock = pygame.time.Clock()
        self.enemy_limit = 1

        pygame.display.set_caption("Battlecity: battlefield")

        self.tile_map = Tilemap(self.level, self.game_surface)
        self.enemy_spawns = self.tile_map.get_enemy_spawns()
        self.hero_spawn = self.tile_map.get_player_spawn()
        self.eagle_spawn = self.tile_map.get_eagle_spawn()

        self.bullets = []
        self.enemies = []

        self.eagle = Eagle(self.game_surface, self.eagle_spawn)
        self.player = Player(self.game_surface, self.hero_spawn, self.tile_map, self.enemies, self.bullets, self.eagle)

        self.side_menu = SideMenu(self.player, self.screen, self.enemy_limit)

        self.enemy_respawn_time = self.get_enemy_respawn_time()
        self.respawn_timer = self.enemy_respawn_time / 30

    def get_enemy_respawn_time(self):
        return (190 - self.level * 4 - (self.player_count - 1) * 20) * 60

    def run(self):
        """Battlefield event loop"""

        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    continue

            self.update_objects()

            self.respawn_timer += 1

            self.clock.tick(30)

    def update_objects(self):
        self.screen.fill(GRAY)
        self.tile_map.update()

        if self.eagle.is_alive:
            self.eagle.update()

        self.update_game_over()
        self.player.update()

        self.update_enemies()
        self.update_bullets()

        self.screen.blit(self.game_surface, (50, 50))
        self.side_menu.update()

        pygame.display.update()

    def update_game_over(self):
        player_is_dead = not self.player.is_alive and self.player.hearts == 0
        eagle_is_dead = not self.eagle.is_alive
        self.game_over = player_is_dead or eagle_is_dead

    def produce_end_text(self):
        if not self.player.is_alive and self.player.hearts == 0 or not self.eagle.is_alive:
            Text("GAME OVER", (338, 338), fontsize=64, color='white').draw(self.game_surface)
            Text("Press space to restart", (338, 378), fontsize=32, color='white').draw(self.game_surface)

        elif len(self.enemies) == 0 and self.enemy_limit == 0:
            Text("YOU WIN", (338, 338), fontsize=64, color='white').draw(self.game_surface)
            Text("Press space to go next level", (328, 378), fontsize=32, color='white').draw(self.game_surface)

    def update_enemies(self):
        self.spawn_enemy()

        for i in range(len(self.enemies)):
            if len(self.enemies) > i:
                self.enemies[i].update()
                if not self.enemies[i].is_alive:
                    self.player.score += 100 * self.enemies[i].enemy_type
                    self.enemies.pop(i)
                    self.side_menu.enemy_icons.pop()

    def spawn_enemy(self):
        if self.respawn_timer >= self.enemy_respawn_time / 30 and self.enemy_limit > 0:
            self.respawn_timer = 0
            self.enemy_limit -= 1
            self.enemies.append(
                Enemy(
                    self.game_surface,
                    self.enemy_spawns[self.enemy_spawn_order],
                    self.tile_map,
                    self.player,
                    self.eagle,
                    self.bullets,
                    self.enemy_respawn_time,
                    self.enemies,
                    EnemyType.LightTank
                )
            )
            self.enemy_spawn_order = (self.enemy_spawn_order + 1) % 2

    def update_bullets(self):
        for i in range(len(self.bullets)):
            if len(self.bullets) > i:
                self.bullets[i].update()
                if not self.bullets[i].is_alive:
                    self.bullets.pop(i)
