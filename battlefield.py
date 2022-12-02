import pygame
from pygame.locals import *

from extra_modules.sound_config import SOUND_PARAMS
from game_objects.bonus import SpeedBonus, HeartBonus, PowerShootingBonus
from game_objects.creatures import (
    Player,
    Enemy,
    Eagle
)

from TileMap import Tilemap
from UI.game_interfaces import SideMenu
from UI.text import Text

from extra_modules.constants import (
    GAME_SURFACE_SIZE,
)


class Battlefield:
    """Game battlefield"""

    def __init__(self, screen, level):
        pygame.init()

        self.level = level

        self.screen = screen
        self.background = pygame.image.load(r'images\UI images\tank_background_1.png').convert_alpha()
        self.game_surface = pygame.Surface(GAME_SURFACE_SIZE)
        pygame.display.set_caption("Battlecity: battlefield")
        self.escape_text = Text("Esc: выход в главное меню", (200, 20), fontsize=32, color=pygame.Color('white'))
        self.load_music()

        self.set_game_objects()
        self.set_game_flags()

        self.clock = pygame.time.Clock()

        self.side_menu = SideMenu(self.player, self.screen, self.enemy_limit)

        self.enemy_respawn_time = self.get_enemy_respawn_time()
        self.respawn_timer = self.enemy_respawn_time / 30

    def load_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(fr'sound_effects\themes\{self.level}.mp3')
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1)

    def set_game_flags(self):
        self.player_count = 1
        self.enemy_spawn_order = 0
        self.running = True
        self.game_over = False
        self.game_win = False
        self.enemy_limit = 10

    def set_game_objects(self):
        self.tile_map_layer_one = Tilemap(str(self.level) + '_1', self.game_surface)
        self.enemy_spawns = self.tile_map_layer_one.get_enemy_spawns()
        self.hero_spawn = self.tile_map_layer_one.get_player_spawn()
        self.eagle_spawn = self.tile_map_layer_one.get_eagle_spawn()

        self.tile_map_layer_two = Tilemap(str(self.level) + '_2', self.game_surface)

        self.bullets = []
        self.enemies = []
        self.bonuses = []
        self.enemy_types = [0, 0, 0, 0, 1, 1, 2, 2, 3, 3]

        self.eagle = Eagle(self.game_surface, self.eagle_spawn)

        self.player = Player(
            self.game_surface,
            self.hero_spawn,
            self.tile_map_layer_one,
            self.enemies,
            self.bullets,
            self.eagle,
            self.bonuses
        )

    def get_enemy_respawn_time(self):
        if self.level != 'test':
            return (190 - self.level * 4 - (self.player_count - 1) * 20) * 60
        return 100

    def run(self):
        """Battlefield event loop"""

        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if pygame.key.get_pressed()[K_ESCAPE]:
                        self.running = False

            self.update_objects()

            self.respawn_timer += 1

            self.clock.tick(30)

        pygame.mixer.music.stop()
        pygame.mixer.music.load('sound_effects\main theme.mp3')
        pygame.mixer.music.set_volume(min(SOUND_PARAMS['general'], SOUND_PARAMS['music']))
        pygame.mixer.music.play(-1)

    def update_objects(self):
        self.screen.blit(self.background, self.screen.get_rect())
        self.tile_map_layer_one.update()
        self.escape_text.draw(self.screen)

        if self.eagle.is_alive:
            self.eagle.update()

        self.update_game_over()

        if self.player.is_alive:
            self.player.update()

        self.update_enemies()
        self.update_bullets()

        for bonus in self.bonuses:
            bonus.update()

        self.tile_map_layer_two.update()

        self.screen.blit(self.game_surface, (50, 50))
        self.side_menu.update()

        pygame.display.update()

    def update_game_over(self):
        player_is_dead = not self.player.is_alive and self.player.hearts == 0
        eagle_is_dead = not self.eagle.is_alive
        self.game_over = player_is_dead or eagle_is_dead
        self.produce_end_text()

    def restart_battlefield(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_r] and self.game_over:
            self.__init__(self.screen, 1)

    def go_next_level(self):
        pressed_keys = pygame.key.get_pressed()
        if self.level == 4:
            self.running = False
        elif pressed_keys[pygame.K_n] and self.game_win:
            self.__init__(self.screen, self.level + 1)

    def produce_end_text(self):
        if not self.player.is_alive and self.player.hearts == 0 or not self.eagle.is_alive:
            Text("GAME OVER", (338, 338), fontsize=64, color='white').draw(self.game_surface)
            Text("Press R to restart", (338, 378), fontsize=32, color='white').draw(self.game_surface)
            self.game_over = True
            self.restart_battlefield()

        elif len(self.enemies) == 0 and self.enemy_limit == 0:
            Text("YOU WIN", (338, 338), fontsize=64, color='white').draw(self.game_surface)
            Text("Press n to go next level", (328, 378), fontsize=32, color='white').draw(self.game_surface)
            self.game_win = True
            self.go_next_level()

    def update_enemies(self):
        self.spawn_enemy()

        for i in range(len(self.enemies)):
            if len(self.enemies) > i:
                self.enemies[i].update()
                if not self.enemies[i].is_alive:
                    self.player.score += self.enemies[i].points
                    self.enemies.pop(i)
                    self.side_menu.enemy_icons.pop()
                    self.spawn_bonus()

    def spawn_bonus(self):
        if self.enemy_limit % 3 == 0:
            self.bonuses.append(PowerShootingBonus(self.game_surface, self.player))
        elif self.enemy_limit % 2 == 0:
            self.bonuses.append(HeartBonus(self.game_surface, self.player))
        else:
            self.bonuses.append(SpeedBonus(self.game_surface, self.player))

    def spawn_enemy(self):
        if self.respawn_timer >= self.enemy_respawn_time / 30 and self.enemy_limit > 0:
            self.respawn_timer = 0
            self.enemy_limit -= 1
            self.enemies.append(
                Enemy(
                    self.game_surface,
                    self.enemy_spawns[self.enemy_spawn_order],
                    self.tile_map_layer_one,
                    self.player,
                    self.eagle,
                    self.bullets,
                    self.enemy_respawn_time,
                    self.enemies,
                    self.enemy_types.pop(0)
                )
            )
            self.enemy_spawn_order = (self.enemy_spawn_order + 1) % len(self.enemy_spawns)

    def update_bullets(self):
        for i in range(len(self.bullets)):
            if len(self.bullets) > i:
                self.bullets[i].update()
                if not self.bullets[i].is_alive and self.bullets[i].frame_counter == -1:
                    self.bullets.pop(i)
